#!/usr/bin/env python3
"""HFACS-BASE classification over the full BFL dataset (production run)."""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

MODEL = "claude-opus-4-6"
MAX_TOKENS = 35000
TEMPERATURE = 0.3
RATE_LIMIT_DELAY = 0.5

BATCH_POLL_INITIAL = 30
BATCH_POLL_MAX = 300
BATCH_POLL_FACTOR = 1.5

LAYERS = ["L0", "L1", "L2"]
L1_INSUFFICIENT_CATEGORY = "103II"

RUN_DIR = Path(__file__).resolve().parent
REPO_ROOT = RUN_DIR.parent
OUTPUTS_DIR = RUN_DIR / "outputs"
INPUT_FILE = REPO_ROOT / "bfl-scrape" / "bfl_fatalities.jsonl"

PROMPTS_DIR = RUN_DIR / "prompts"
BASE_SYSTEM_FILE = PROMPTS_DIR / "base_system.md"
DOMAIN_CONTEXT_FILE = RUN_DIR / "BASE_DOMAIN_CONTEXT.md"
HFACS_FILES = {
    "L0": PROMPTS_DIR / "HFACS_L0.md",
    "L1": PROMPTS_DIR / "HFACS_L1.md",
    "L2": PROMPTS_DIR / "HFACS_L2.md",
}

log = logging.getLogger("hfacs")

# Name is excluded from the model input for privacy.
STRUCTURED_FIELDS = [
    "BFL entry nr.", "Date", "Time", "Age", "Nationality", "Location",
    "Category", "Object Type", "Base seasons", "Skydives", "WS Skydives",
    "BASE Jumps", "WS BASE Jumps", "Clothing - Suit", "Canopy", "Container",
    "Packing & Setup", "Weather", "Possible Factors", "Cause of Death",
]


def load_records(path, limit=None):
    records = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
                if limit and len(records) >= limit:
                    break
    log.info("Loaded %d records from %s", len(records), path)
    return records


def load_layer_results(layer):
    path = OUTPUTS_DIR / f"{layer}_results.jsonl"
    if not path.exists():
        log.error("Required results file not found: %s", path)
        sys.exit(1)
    results = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                results[rec["record_id"]] = rec
    log.info("Loaded %d %s results", len(results), layer)
    return results


def fmt_value(value):
    if value is None:
        return "Not reported"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "Not reported"
    return str(value)


def format_user_message(record):
    lines = ["Classify the following BASE jumping fatality report.\n"]
    lines += [f"{field}: {fmt_value(record.get(field))}" for field in STRUCTURED_FIELDS]
    lines.append("")
    lines.append(f"Accident narrative:\n{record.get('Accident', 'Not reported')}")
    return "\n".join(lines)


def format_l2_message(record, l1_result):
    base = format_user_message(record)
    acts = l1_result.get("L1_unsafe_acts", [])
    if acts:
        act_lines = [f"[{a['category']}] {a.get('label', '')}: {a.get('description', '')}" for a in acts]
        base += "\n\nLayer 1 unsafe acts identified:\n" + "\n".join(act_lines)
    return base


def build_system_prompt(layer):
    # One cached text block so the ~28k-token prefix is read from cache
    # on every record after the first.
    base = BASE_SYSTEM_FILE.read_text()
    domain = DOMAIN_CONTEXT_FILE.read_text()
    hfacs = HFACS_FILES[layer].read_text()
    text = f"{base}\n\n{domain}\n\n{hfacs}"
    return [
        {
            "type": "text",
            "text": text,
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        }
    ]


def system_prompt_chars(system_prompt):
    return sum(len(b["text"]) for b in system_prompt)


def parse_response(response):
    text = None
    for block in response.content:
        if block.type == "text":
            text = block.text

    stop_reason = response.stop_reason

    if stop_reason == "max_tokens":
        log.warning("Response truncated (max_tokens reached)")
        return None, {
            "cause": "max_tokens",
            "stop_reason": stop_reason,
            "raw_text_preview": (text[:500] if text else None),
        }

    if not text:
        return None, {
            "cause": "no_text",
            "stop_reason": stop_reason,
            "raw_text_preview": None,
        }

    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        stripped = "\n".join(lines).strip()

    obj_start = stripped.find("{")
    if obj_start == -1:
        return None, {
            "cause": "json_parse",
            "stop_reason": stop_reason,
            "parse_error": "no '{' found in text",
            "raw_text_preview": text[:500],
        }

    try:
        result, end = json.JSONDecoder().raw_decode(stripped[obj_start:])
        trailing = stripped[obj_start + end:].strip()
        if trailing:
            log.info("Ignored %d chars of trailing content after JSON", len(trailing))
        return result, None
    except json.JSONDecodeError as e:
        log.warning("JSON parse error: %s — raw: %.300s", e, text)
        return None, {
            "cause": "json_parse",
            "stop_reason": stop_reason,
            "parse_error": str(e),
            "raw_text_preview": text[:500],
        }


def call_live(client, system_prompt, user_msg):
    # Streaming is required: prefix + max_tokens can exceed the 10-minute
    # non-streaming ceiling.
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        return stream.get_final_message()


def run_layer_live(client, system_prompt, messages):
    results = []
    total = len(messages)
    for i, (rid, msg) in enumerate(messages):
        log.info("[%d/%d] %s", i + 1, total, rid)
        try:
            resp = call_live(client, system_prompt, msg)
            results.append((rid, resp, None))
        except Exception as e:
            log.error("API error for %s: %s", rid, e)
            results.append((rid, None, str(e)))
        if i < total - 1:
            time.sleep(RATE_LIMIT_DELAY)
    return results


def warmup_cache(client, system_prompt):
    # Anthropic's batch docs: "a cache entry only becomes available after the
    # first response begins. If you need cache hits for parallel requests,
    # wait for the first response before sending subsequent requests."
    # Without this warmup, each parallel batch request would write its own
    # cache entry rather than share a single read.
    log.info("Warming prompt cache...")
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=16,
            temperature=TEMPERATURE,
            system=system_prompt,
            messages=[{"role": "user", "content": "ready"}],
        )
        usage = resp.usage
        log.info(
            "Cache warmed: creation=%s read=%s",
            getattr(usage, "cache_creation_input_tokens", "?"),
            getattr(usage, "cache_read_input_tokens", "?"),
        )
    except Exception as e:
        log.warning("Cache warmup failed (%s); batch may not hit cache", e)


def run_layer_batch(client, system_prompt, messages, layer):
    warmup_cache(client, system_prompt)

    requests = [
        {
            "custom_id": rid,
            "params": {
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
                "system": system_prompt,
                "messages": [{"role": "user", "content": msg}],
            },
        }
        for rid, msg in messages
    ]

    log.info("Submitting %s batch: %d requests", layer, len(requests))
    batch = client.messages.batches.create(requests=requests)
    log.info("Batch %s created (%s)", batch.id, batch.processing_status)

    # Persist batch id so a failed/interrupted run can recover results manually.
    (OUTPUTS_DIR / f"{layer}_batch_id.txt").write_text(batch.id + "\n")

    delay = BATCH_POLL_INITIAL
    while batch.processing_status != "ended":
        log.info("Batch %s: %s — next poll in %ds",
                 batch.id, batch.processing_status, int(delay))
        time.sleep(delay)
        delay = min(delay * BATCH_POLL_FACTOR, BATCH_POLL_MAX)
        batch = client.messages.batches.retrieve(batch.id)

    log.info("Batch %s ended. Counts: %s", batch.id, batch.request_counts)

    results_map = {}
    for entry in client.messages.batches.results(batch.id):
        rid = entry.custom_id
        if entry.result.type == "succeeded":
            results_map[rid] = (entry.result.message, None)
        else:
            err = getattr(entry.result, "error", entry.result.type)
            log.error("Batch failed for %s: %s", rid, err)
            results_map[rid] = (None, str(err))

    return [(rid, *results_map.get(rid, (None, "missing from batch results")))
            for rid, _ in messages]


def get_record_id(record):
    return record["BFL entry nr."]


def write_jsonl(path, items):
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")


def append_error(rid, layer, error_info):
    entry = {
        "record_id": rid,
        "layer": layer,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        **error_info,
    }
    with open(OUTPUTS_DIR / "errors.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")


def _l1_has_actionable_act(l1_rec):
    acts = l1_rec.get("L1_unsafe_acts") or []
    return any(a.get("category") != L1_INSUFFICIENT_CATEGORY for a in acts)


def run_layer(client, layer, records, mode, l0_results=None, l1_results=None, only=None):
    if layer == "L0":
        eligible = records
    elif layer == "L1":
        eligible = [
            r for r in records
            if l0_results.get(get_record_id(r), {}).get("L0_classification") == "001HE"
        ]
        log.info("L1: %d records with L0=001HE", len(eligible))
    elif layer == "L2":
        eligible = [
            r for r in records
            if get_record_id(r) in l1_results
            and _l1_has_actionable_act(l1_results[get_record_id(r)])
        ]
        log.info("L2: %d records with at least one non-%s L1 act",
                 len(eligible), L1_INSUFFICIENT_CATEGORY)

    if only is not None:
        missing = only - {get_record_id(r) for r in eligible}
        if missing:
            log.warning("%s: --only records not eligible at this layer: %s",
                        layer, sorted(missing))
        eligible = [r for r in eligible if get_record_id(r) in only]
        log.info("%s: --only filter → %d records this run", layer, len(eligible))

    if not eligible:
        log.warning("No eligible records for %s", layer)
        return {}

    system_prompt = build_system_prompt(layer)
    log.info(
        "%s: system prompt %d chars, %d eligible records",
        layer, system_prompt_chars(system_prompt), len(eligible),
    )

    messages = []
    for r in eligible:
        rid = get_record_id(r)
        if layer == "L2":
            msg = format_l2_message(r, l1_results[rid])
        else:
            msg = format_user_message(r)
        messages.append((rid, msg))

    if mode == "live":
        raw = run_layer_live(client, system_prompt, messages)
    else:
        raw = run_layer_batch(client, system_prompt, messages, layer)

    parsed = {}
    cause_counts = {"max_tokens": 0, "json_parse": 0, "no_text": 0, "api_error": 0}
    succeeded = 0

    for rid, response, api_error in raw:
        if response is None:
            err = {
                "cause": "api_error",
                "stop_reason": None,
                "api_error": api_error,
                "raw_text_preview": None,
            }
            cause_counts["api_error"] += 1
            append_error(rid, layer, err)
            parsed[rid] = {"record_id": rid, "_error": err}
            continue

        result, err = parse_response(response)

        if err is not None:
            cause_counts[err["cause"]] += 1
            append_error(rid, layer, err)
            parsed[rid] = {"record_id": rid, "_error": err}
            continue

        result["record_id"] = rid
        parsed[rid] = result
        succeeded += 1

    out_path = OUTPUTS_DIR / f"{layer}_results.jsonl"
    if only is not None and out_path.exists():
        existing = {}
        with open(out_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    rec = json.loads(line)
                    existing[rec["record_id"]] = rec
        existing.update(parsed)
        write_jsonl(out_path, list(existing.values()))
    else:
        write_jsonl(out_path, list(parsed.values()))

    skipped = len(records) - len(eligible)
    failed = sum(cause_counts.values())
    log.info(
        "%s done — eligible: %d, succeeded: %d, failed: %d "
        "(max_tokens=%d, json_parse=%d, no_text=%d, api_error=%d), skipped: %d",
        layer, len(eligible), succeeded, failed,
        cause_counts["max_tokens"], cause_counts["json_parse"],
        cause_counts["no_text"], cause_counts["api_error"], skipped,
    )
    return parsed


def merge_results():
    l0 = load_layer_results("L0")
    l1_path = OUTPUTS_DIR / "L1_results.jsonl"
    l1 = load_layer_results("L1") if l1_path.exists() else {}
    l2_path = OUTPUTS_DIR / "L2_results.jsonl"
    l2 = load_layer_results("L2") if l2_path.exists() else {}

    merged = []
    for rid, l0_rec in l0.items():
        entry = {
            "record_id": rid,
            "L0_classification": l0_rec.get("L0_classification"),
            "L0_label": l0_rec.get("L0_label"),
            "L0_description": l0_rec.get("L0_description"),
            "L1_unsafe_acts": None,
            "L2_preconditions": None,
            "errors": {},
        }
        if "_error" in l0_rec:
            entry["errors"]["L0"] = l0_rec["_error"]
        if rid in l1:
            entry["L1_unsafe_acts"] = l1[rid].get("L1_unsafe_acts")
            if "_error" in l1[rid]:
                entry["errors"]["L1"] = l1[rid]["_error"]
        if rid in l2:
            entry["L2_preconditions"] = l2[rid].get("L2_preconditions")
            if "_error" in l2[rid]:
                entry["errors"]["L2"] = l2[rid]["_error"]
        if not entry["errors"]:
            del entry["errors"]
        merged.append(entry)

    out = OUTPUTS_DIR / "classification_results.jsonl"
    write_jsonl(out, merged)
    log.info("Merged %d records → %s", len(merged), out)


def main():
    parser = argparse.ArgumentParser(description="HFACS-BASE full BFL classification")
    parser.add_argument("--mode", choices=["live", "batch"], default="batch",
                        help="batch (default, 50%% cost, 24h SLA) or live (streaming, for smoke tests)")
    parser.add_argument("--layer", choices=["L0", "L1", "L2", "all"], default="all")
    parser.add_argument("--limit", type=int, default=None,
                        help="Process only first N records (for testing)")
    parser.add_argument("--only", type=str, default=None,
                        help="Comma-separated record IDs to re-run.")
    args = parser.parse_args()

    only = None
    if args.only:
        only = {rid.strip() for rid in args.only.split(",") if rid.strip()}

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    load_dotenv(REPO_ROOT / ".env")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY not set (looked in environment and %s)",
                  REPO_ROOT / ".env")
        sys.exit(1)

    client = anthropic.Anthropic()
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    log.info("Run output dir: %s", OUTPUTS_DIR)
    log.info("Config: model=%s, mode=%s, temperature=%s", MODEL, args.mode, TEMPERATURE)

    errors_path = OUTPUTS_DIR / "errors.jsonl"
    if errors_path.exists():
        if only is None:
            errors_path.unlink()
        else:
            kept = []
            with open(errors_path) as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    e = json.loads(line)
                    if e.get("record_id") not in only:
                        kept.append(e)
            write_jsonl(errors_path, kept)

    records = load_records(INPUT_FILE, args.limit)
    layers_to_run = LAYERS if args.layer == "all" else [args.layer]

    l0_results = None
    l1_results = None

    for layer in layers_to_run:
        if layer in ("L1", "L2") and l0_results is None:
            l0_results = load_layer_results("L0")
        if layer == "L2" and l1_results is None:
            l1_results = load_layer_results("L1")

        results = run_layer(
            client, layer, records, args.mode,
            l0_results=l0_results, l1_results=l1_results,
            only=only,
        )

        if layer == "L0":
            l0_results = load_layer_results("L0") if (OUTPUTS_DIR / "L0_results.jsonl").exists() else results
        elif layer == "L1":
            l1_results = load_layer_results("L1") if (OUTPUTS_DIR / "L1_results.jsonl").exists() else results

    if (OUTPUTS_DIR / "L0_results.jsonl").exists():
        merge_results()


if __name__ == "__main__":
    main()
