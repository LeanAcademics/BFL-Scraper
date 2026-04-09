#!/usr/bin/env python3
"""
HFACS-BASE Classification Pipeline

Classifies BASE jumping fatality reports through a three-layer HFACS framework
using LLM analysis via the Anthropic API.

Layers:
  L0 — Top-level classification (human error / other cause / insufficient info)
  L1 — Unsafe acts (runs on L0=001HE records only)
  L2 — Preconditions for unsafe acts (runs on records with L1 results)
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import anthropic

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "claude-opus-4-6"
TEMPERATURE = 0.3
MAX_TOKENS = 16000
THINKING = {"type": "adaptive"}
RATE_LIMIT_DELAY = 0.5  # seconds between live API calls

LAYERS = ["L0", "L1", "L2"]

PIPELINE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = PIPELINE_DIR / "prompts"
OUTPUTS_DIR = PIPELINE_DIR / "outputs"
INPUT_FILE = PIPELINE_DIR.parent / "bfl-scrape" / "bfl_fatalities.jsonl"
DOMAIN_CONTEXT_FILE = PIPELINE_DIR / "BASE_DOMAIN_CONTEXT.md"
HFACS_FILES = {
    "L0": PROMPTS_DIR / "HFACS_L0.md",
    "L1": PROMPTS_DIR / "HFACS_L1.md",
    "L2": PROMPTS_DIR / "HFACS_L2.md",
}

BATCH_POLL_INITIAL = 30    # seconds
BATCH_POLL_MAX = 300       # seconds
BATCH_POLL_FACTOR = 1.5

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
    """Assemble system prompt: base + domain context + layer-specific HFACS prompt."""
    base = (PROMPTS_DIR / "base_system.md").read_text()
    domain = DOMAIN_CONTEXT_FILE.read_text()
    hfacs = HFACS_FILES[layer].read_text()
    return f"{base}\n\n{domain}\n\n{hfacs}"


# ---------------------------------------------------------------------------
# Response parsing
# ---------------------------------------------------------------------------

def parse_response(response):
    """
    Extract classification JSON and thinking text from an API response.
    Returns (parsed_json, thinking_text). Either may be None.
    """
    thinking = None
    text = None

    for block in response.content:
        if block.type == "thinking":
            thinking = block.thinking
        elif block.type == "text":
            text = block.text

    if response.stop_reason == "max_tokens":
        log.warning("Response truncated (max_tokens reached)")

    if not text:
        return None, thinking

    # Strip markdown fences if the model added them despite instructions
    stripped = text.strip()
    if stripped.startswith("```"):
        lines = stripped.split("\n")
        lines = lines[1:]  # drop opening fence line
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]  # drop closing fence line
        stripped = "\n".join(lines).strip()

    try:
        return json.loads(stripped), thinking
    except json.JSONDecodeError as e:
        log.warning("JSON parse error: %s — raw: %.300s", e, text)
        return None, thinking


# ---------------------------------------------------------------------------
# Live mode
# ---------------------------------------------------------------------------

def call_live(client, system_prompt, user_msg):
    """Make a single synchronous API call."""
    return client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        thinking=THINKING,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )


def run_layer_live(client, system_prompt, messages):
    """
    Process all messages sequentially with rate limiting.
    messages: list of (record_id, user_message) tuples.
    Returns list of (record_id, response_or_None).
    """
    results = []
    total = len(messages)
    for i, (rid, msg) in enumerate(messages):
        log.info("[%d/%d] %s", i + 1, total, rid)
        try:
            resp = call_live(client, system_prompt, msg)
            results.append((rid, resp))
        except Exception as e:
            log.error("API error for %s: %s", rid, e)
            results.append((rid, None))
        if i < total - 1:
            time.sleep(RATE_LIMIT_DELAY)
    return results


# ---------------------------------------------------------------------------
# Batch mode
# ---------------------------------------------------------------------------

def run_layer_batch(client, system_prompt, messages):
    """
    Submit all messages as a single batch, poll for completion, collect results.
    messages: list of (record_id, user_message) tuples.
    Returns list of (record_id, response_or_None).
    """
    requests = [
        {
            "custom_id": rid,
            "params": {
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "temperature": TEMPERATURE,
                "thinking": THINKING,
                "system": system_prompt,
                "messages": [{"role": "user", "content": msg}],
            },
        }
        for rid, msg in messages
    ]

    log.info("Submitting batch: %d requests", len(requests))
    batch = client.messages.batches.create(requests=requests)
    log.info("Batch %s created (%s)", batch.id, batch.processing_status)

    # Poll until batch processing ends
    delay = BATCH_POLL_INITIAL
    while batch.processing_status != "ended":
        log.info("Batch %s: %s — next poll in %ds",
                 batch.id, batch.processing_status, int(delay))
        time.sleep(delay)
        delay = min(delay * BATCH_POLL_FACTOR, BATCH_POLL_MAX)
        batch = client.messages.batches.retrieve(batch.id)

    log.info("Batch %s ended. Counts: %s", batch.id, batch.request_counts)

    # Collect results keyed by custom_id
    results_map = {}
    for entry in client.messages.batches.results(batch.id):
        rid = entry.custom_id
        if entry.result.type == "succeeded":
            results_map[rid] = entry.result.message
        else:
            error_detail = getattr(entry.result, "error", entry.result.type)
            log.error("Batch failed for %s: %s", rid, error_detail)
            results_map[rid] = None

    # Return in original submission order
    return [(rid, results_map.get(rid)) for rid, _ in messages]


# ---------------------------------------------------------------------------
# Layer orchestration
# ---------------------------------------------------------------------------

def get_record_id(record):
    return record["BFL entry nr."]


def write_jsonl(path, items):
    with open(path, "w") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")


def append_error(rid, layer, error):
    entry = {
        "record_id": rid,
        "layer": layer,
        "error": str(error),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    with open(OUTPUTS_DIR / "errors.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")


def run_layer(client, layer, records, mode, l0_results=None, l1_results=None):
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
    log.info("%s: system prompt %d chars, %d eligible records", layer, len(system_prompt), len(eligible))

    # Build (record_id, user_message) pairs
    messages = []
    for r in eligible:
        rid = get_record_id(r)
        if layer == "L2":
            msg = format_l2_message(r, l1_results[rid])
        else:
            msg = format_user_message(r)
        messages.append((rid, msg))

    # Dispatch to live or batch
    if mode == "live":
        raw = run_layer_live(client, system_prompt, messages)
    else:
        raw = run_layer_batch(client, system_prompt, messages)

    # Parse responses and collect results
    parsed = {}
    thinking_entries = []
    failed = 0

    for rid, response in raw:
        if response is None:
            failed += 1
            append_error(rid, layer, "No response from API")
            continue

        result, thinking = parse_response(response)
        if result is None:
            failed += 1
            append_error(rid, layer, "Failed to parse JSON from response")
            continue

        # Ensure record_id is correct regardless of LLM output
        result["record_id"] = rid
        parsed[rid] = result

        if thinking:
            thinking_entries.append({"record_id": rid, "thinking": thinking})

    # Write intermediate outputs
    write_jsonl(OUTPUTS_DIR / f"{layer}_results.jsonl", list(parsed.values()))
    write_jsonl(OUTPUTS_DIR / f"{layer}_thinking.jsonl", thinking_entries)

    skipped = len(records) - len(eligible)
    log.info(
        "%s done — eligible: %d, succeeded: %d, failed: %d, skipped: %d",
        layer, len(eligible), len(parsed), failed, skipped,
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
        }
        if rid in l1:
            entry["L1_unsafe_acts"] = l1[rid].get("L1_unsafe_acts")
            entry["L1_insufficient"] = l1[rid].get("L1_insufficient")
        if rid in l2:
            entry["L2_preconditions"] = l2[rid].get("L2_preconditions")
        merged.append(entry)

    out = OUTPUTS_DIR / "classification_results.jsonl"
    write_jsonl(out, merged)
    log.info("Merged %d records → %s", len(merged), out)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="HFACS-BASE classification pipeline")
    parser.add_argument("--mode", choices=["live", "batch"], default="live",
                        help="API mode: live (sequential) or batch (50%% cost reduction)")
    parser.add_argument("--layer", choices=["L0", "L1", "L2", "all"], default="all",
                        help="Layer to run (default: all)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Process only first N records (for testing)")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    if not os.environ.get("ANTHROPIC_API_KEY"):
        log.error("ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic()
    OUTPUTS_DIR.mkdir(exist_ok=True)

    # Clear errors file at start of run
    errors_path = OUTPUTS_DIR / "errors.jsonl"
    if errors_path.exists():
        errors_path.unlink()

    records = load_records(INPUT_FILE, args.limit)
    layers_to_run = LAYERS if args.layer == "all" else [args.layer]

    l0_results = None
    l1_results = None

    for layer in layers_to_run:
        # Load previous layer results from disk if not already in memory
        if layer == "L1" and l0_results is None:
            l0_results = load_layer_results("L0")
        if layer == "L2" and l1_results is None:
            l1_results = load_layer_results("L1")

        results = run_layer(
            client, layer, records, args.mode,
            l0_results=l0_results, l1_results=l1_results,
        )

        # Keep in memory for subsequent layers in this run
        if layer == "L0":
            l0_results = results
        elif layer == "L1":
            l1_results = results

    # Merge whenever L0 results exist on disk
    if (OUTPUTS_DIR / "L0_results.jsonl").exists():
        merge_results()


if __name__ == "__main__":
    main()
