#!/usr/bin/env python3
"""
HFACS-BASE Synthetic Validation Pipeline

Runs the same three-layer HFACS classification as the main pipeline but against
the 30-record synthetic dataset. Uses live mode only (no batch needed).
Reads prompts and domain context from the main classification-pipeline.
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "claude-opus-4-6"
MAX_TOKENS = 35000
THINKING = {"type": "adaptive"}
RATE_LIMIT_DELAY = 0.5

LAYERS = ["L0", "L1", "L2"]

PIPELINE_DIR = Path(__file__).resolve().parent
MAIN_PIPELINE_DIR = PIPELINE_DIR.parent / "classification-pipeline"
PROMPTS_DIR = MAIN_PIPELINE_DIR / "prompts"
RUNS_DIR = PIPELINE_DIR / "synthetic-data-output" / "runs"
INPUT_FILE = PIPELINE_DIR / "synthetic-data-output" / "synthetic-bfl.jsonl"
DOMAIN_CONTEXT_FILE = MAIN_PIPELINE_DIR / "BASE_DOMAIN_CONTEXT.md"
HFACS_FILES = {
    "L0": PROMPTS_DIR / "HFACS_L0.md",
    "L1": PROMPTS_DIR / "HFACS_L1.md",
    "L2": PROMPTS_DIR / "HFACS_L2.md",
}

log = logging.getLogger("hfacs")

# Fields included in user messages (Name excluded for privacy)
STRUCTURED_FIELDS = [
    "BFL entry nr.", "Date", "Time", "Age", "Nationality", "Location",
    "Category", "Object Type", "Base seasons", "Skydives", "WS Skydives",
    "BASE Jumps", "WS BASE Jumps", "Clothing - Suit", "Canopy", "Container",
    "Packing & Setup", "Weather", "Possible Factors", "Cause of Death",
]


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_records(path, limit=None):
    """Read JSONL input file, return list of record dicts."""
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
    """Load a layer's intermediate results from disk, keyed by record_id."""
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


# ---------------------------------------------------------------------------
# Message formatting
# ---------------------------------------------------------------------------

def fmt_value(value):
    """Format a field value for the user message."""
    if value is None:
        return "Not reported"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "Not reported"
    return str(value)


def format_user_message(record):
    """Format a BFL record as user message text. Excludes Name for privacy."""
    lines = ["Classify the following BASE jumping fatality report.\n"]
    lines += [f"{field}: {fmt_value(record.get(field))}" for field in STRUCTURED_FIELDS]
    lines.append("")
    lines.append(f"Accident narrative:\n{record.get('Accident', 'Not reported')}")
    return "\n".join(lines)


def format_l2_message(record, l1_result):
    """Format user message for L2: base record + appended L1 findings."""
    base = format_user_message(record)
    acts = l1_result.get("L1_unsafe_acts", [])
    if acts:
        act_lines = [f"[{a['category']}] {a['label']}: {a['description']}" for a in acts]
        base += "\n\nLayer 1 unsafe acts identified:\n" + "\n".join(act_lines)
    return base


# ---------------------------------------------------------------------------
# System prompt construction
# ---------------------------------------------------------------------------

def build_system_prompt(layer):
    """
    Assemble system prompt: base + domain context + layer-specific HFACS prompt.
    Returned as a single text block with 1h ephemeral cache_control so the
    ~28k-token prefix is read from cache on every record after the first.
    """
    base = (PROMPTS_DIR / "base_system.md").read_text()
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
    """Total character count across all blocks of a structured system prompt."""
    return sum(len(b["text"]) for b in system_prompt)


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def parse_response(response):
    """
    Extract classification JSON and thinking text from an API response.

    Returns (result, thinking, error_info):
      - result:    parsed JSON dict, or None on failure
      - thinking:  thinking-block text, or None
      - error_info: None on success, otherwise a dict with cause/stop_reason/...
                    where cause ∈ {"max_tokens", "no_text", "json_parse"}
    """
    thinking = None
    text = None

    for block in response.content:
        if block.type == "thinking":
            thinking = block.thinking
        elif block.type == "text":
            text = block.text

    stop_reason = response.stop_reason

    # Truncation: response cut off before the JSON answer was complete
    if stop_reason == "max_tokens":
        log.warning("Response truncated (max_tokens reached)")
        return None, thinking, {
            "cause": "max_tokens",
            "stop_reason": stop_reason,
            "raw_text_preview": (text[:500] if text else None),
        }

    # No visible text returned at all (rare — usually a refusal or empty response)
    if not text:
        return None, thinking, {
            "cause": "no_text",
            "stop_reason": stop_reason,
            "raw_text_preview": None,
        }

    # Strip markdown fences if the model added them despite instructions
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        lines = lines[1:]  # drop opening fence line
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # drop closing fence line
        stripped = "\n".join(lines).strip()

    try:
        return json.loads(stripped), thinking, None
    except json.JSONDecodeError as e:
        log.warning("JSON parse error: %s — raw: %.300s", e, text)
        return None, thinking, {
            "cause": "json_parse",
            "stop_reason": stop_reason,
            "parse_error": str(e),
            "raw_text_preview": text[:500],
        }


# ---------------------------------------------------------------------------
# Live mode
# ---------------------------------------------------------------------------

def call_live(client, system_prompt, user_msg):
    """Make a single API call using streaming (required for extended thinking with large prompts)."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking=THINKING,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    ) as stream:
        return stream.get_final_message()


def run_layer_live(client, system_prompt, messages):
    """
    Process all messages sequentially with rate limiting.
    messages: list of (record_id, user_message) tuples.
    Returns list of (record_id, response_or_None, api_error_or_None).
    """
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


# ---------------------------------------------------------------------------
# Layer orchestration
# ---------------------------------------------------------------------------

def get_record_id(record):
    return record["BFL entry nr."]


def write_jsonl(path, items):
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")


def append_error(rid, layer, error_info):
    """
    Append a structured error entry to errors.jsonl.

    error_info is a dict with at minimum a `cause` field, one of:
      - "max_tokens"  : response truncated before JSON answer completed
      - "json_parse"  : response complete but JSON could not be parsed
      - "no_text"     : response had no text block (e.g. refusal, empty)
      - "api_error"   : the API call itself failed (live exception or batch failure)
    Other fields may include: stop_reason, raw_text_preview, parse_error, api_error.
    """
    entry = {
        "record_id": rid,
        "layer": layer,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        **error_info,
    }
    with open(OUTPUTS_DIR / "errors.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")


def run_layer(client, layer, records, l0_results=None, l1_results=None):
    """
    Run classification for one layer.
    Returns dict of {record_id: parsed_result}.
    """
    # Determine eligible records
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
            and l1_results[get_record_id(r)].get("L1_unsafe_acts")
        ]
        log.info("L2: %d records with non-empty L1 unsafe acts", len(eligible))

    if not eligible:
        log.warning("No eligible records for %s", layer)
        return {}

    # Build system prompt once for the entire layer
    system_prompt = build_system_prompt(layer)
    log.info(
        "%s: system prompt %d chars, %d eligible records",
        layer, system_prompt_chars(system_prompt), len(eligible),
    )

    # Build (record_id, user_message) pairs
    messages = []
    for r in eligible:
        rid = get_record_id(r)
        if layer == "L2":
            msg = format_l2_message(r, l1_results[rid])
        else:
            msg = format_user_message(r)
        messages.append((rid, msg))

    raw = run_layer_live(client, system_prompt, messages)

    # Parse responses and collect results.
    # Failed records are NOT dropped — they're written with an _error marker so
    # downstream analysis can find them and re-run only the affected records.
    parsed = {}
    thinking_entries = []
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

        result, thinking, err = parse_response(response)

        if thinking:
            thinking_entries.append({"record_id": rid, "thinking": thinking})

        if err is not None:
            cause_counts[err["cause"]] += 1
            append_error(rid, layer, err)
            parsed[rid] = {"record_id": rid, "_error": err}
            continue

        # Ensure record_id is correct regardless of LLM output
        result["record_id"] = rid
        parsed[rid] = result
        succeeded += 1

    # Write intermediate outputs
    write_jsonl(OUTPUTS_DIR / f"{layer}_results.jsonl", list(parsed.values()))
    write_jsonl(OUTPUTS_DIR / f"{layer}_thinking.jsonl", thinking_entries)

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


# ---------------------------------------------------------------------------
# Merge
# ---------------------------------------------------------------------------

def merge_results():
    """Merge L0/L1/L2 results into final classification_results.jsonl (no thinking)."""
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
            "L0_description": l0_rec.get("L0_description"),
            "L1_unsafe_acts": None,
            "L1_insufficient": None,
            "L2_preconditions": None,
            "errors": {},
        }
        if "_error" in l0_rec:
            entry["errors"]["L0"] = l0_rec["_error"]
        if rid in l1:
            entry["L1_unsafe_acts"] = l1[rid].get("L1_unsafe_acts")
            entry["L1_insufficient"] = l1[rid].get("L1_insufficient")
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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    global OUTPUTS_DIR

    parser = argparse.ArgumentParser(description="HFACS-BASE synthetic validation pipeline")
    parser.add_argument("--run", required=True,
                        help="Run name (e.g. claude-run-1, openai-run-1)")
    parser.add_argument("--layer", choices=["L0", "L1", "L2", "all"], default="all",
                        help="Layer to run (default: all)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Process only first N records (for testing)")
    args = parser.parse_args()

    OUTPUTS_DIR = RUNS_DIR / args.run

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    load_dotenv(PIPELINE_DIR.parent / ".env")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY not set (looked in environment and %s)",
                  PIPELINE_DIR.parent / ".env")
        sys.exit(1)

    client = anthropic.Anthropic()
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    log.info("Run: %s → %s", args.run, OUTPUTS_DIR)

    errors_path = OUTPUTS_DIR / "errors.jsonl"
    if errors_path.exists():
        errors_path.unlink()

    records = load_records(INPUT_FILE, args.limit)
    layers_to_run = LAYERS if args.layer == "all" else [args.layer]

    l0_results = None
    l1_results = None

    for layer in layers_to_run:
        if layer == "L1" and l0_results is None:
            l0_results = load_layer_results("L0")
        if layer == "L2" and l1_results is None:
            l1_results = load_layer_results("L1")

        results = run_layer(
            client, layer, records,
            l0_results=l0_results, l1_results=l1_results,
        )

        if layer == "L0":
            l0_results = results
        elif layer == "L1":
            l1_results = results

    if (OUTPUTS_DIR / "L0_results.jsonl").exists():
        merge_results()


if __name__ == "__main__":
    main()
