#!/usr/bin/env python3
"""
Render per-record pipeline output vs. ground truth to markdown for human review.

Reads:
  ./output/L0_results.jsonl
  ./output/L1_results.jsonl
  ./output/L2_results.jsonl
  ./ground-truth.jsonl
  ./output/comparison.jsonl
Writes:
  ./output-readable/per-record-results.md
  ./output-readable/ground-truth.md
  ./output-readable/summary.md
"""

import json
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
OUT_DIR = RUN_DIR / "output"
READABLE_DIR = RUN_DIR / "output-readable"


def load_jsonl(path):
    records = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            records[r["record_id"]] = r
    return records


def fmt_l1_pipeline(l1_rec):
    if not l1_rec:
        return "_no L1 stage run_"
    acts = l1_rec.get("L1_unsafe_acts") or []
    if not acts:
        return "_(empty)_"
    parts = []
    for a in acts:
        cat = a.get("category", "?")
        label = a.get("label", "")
        desc = a.get("description", "")
        line = f"- `{cat}` — **{label}**"
        if desc:
            line += f"\n  > {desc}"
        parts.append(line)
    return "\n".join(parts)


def fmt_l1_gt(gt_rec):
    acts = gt_rec.get("L1_unsafe_acts")
    if acts is None:
        return "_N/A (L0 ≠ 001HE)_"
    if not acts:
        return "_(empty)_"
    return "\n".join(f"- `{a['category']}` — {a.get('label', '')}" for a in acts)


def fmt_l2_pipeline(l2_rec):
    if not l2_rec:
        return "_no L2 stage run_"
    preconds = l2_rec.get("L2_preconditions") or []
    if not preconds:
        return "_(empty)_"
    parts = []
    for p in preconds:
        sub = p.get("subcategory") or p.get("category", "?")
        linked = p.get("linked_L1", "?")
        label = p.get("label", "")
        desc = p.get("description", "")
        line = f"- `{sub}` → `{linked}` — **{label}**"
        if desc:
            line += f"\n  > {desc}"
        parts.append(line)
    return "\n".join(parts)


def fmt_l2_gt(gt_rec):
    preconds = gt_rec.get("L2_preconditions")
    if preconds is None:
        return "_N/A (L0 ≠ 001HE)_"
    if not preconds:
        return "_(empty)_"
    return "\n".join(
        f"- `{p.get('subcategory') or p.get('category')}` → `{p.get('linked_L1', '?')}` — {p.get('label', '')}"
        for p in preconds
    )


def main():
    READABLE_DIR.mkdir(parents=True, exist_ok=True)

    l0 = load_jsonl(OUT_DIR / "L0_results.jsonl")
    l1 = load_jsonl(OUT_DIR / "L1_results.jsonl") if (OUT_DIR / "L1_results.jsonl").exists() else {}
    l2 = load_jsonl(OUT_DIR / "L2_results.jsonl") if (OUT_DIR / "L2_results.jsonl").exists() else {}
    gt = load_jsonl(RUN_DIR / "ground-truth.jsonl")
    comp = load_jsonl(OUT_DIR / "comparison.jsonl") if (OUT_DIR / "comparison.jsonl").exists() else {}

    ids = sorted(gt.keys(), key=lambda x: int(x.replace("BFL", "")))

    # -----------------------------------------------------------------------
    # per-record-results.md
    # -----------------------------------------------------------------------
    lines = [
        "# Manual-Subset Pipeline — Per-Record Results",
        "",
        f"Opus 4.6, temperature 0.3, n={len(ids)}. Pipeline output paired with ground truth for each record.",
        "",
        "Legend: ✓ = match, ✗ = mismatch (set-based, parent-category or subcategory as shown).",
        "",
        "---",
        "",
    ]

    for rid in ids:
        gt_rec = gt[rid]
        l0_rec = l0.get(rid, {})
        l1_rec = l1.get(rid)
        l2_rec = l2.get(rid)
        comp_rec = comp.get(rid, {})

        gt_l0 = gt_rec["L0_classification"]
        pipe_l0 = l0_rec.get("L0_classification")
        l0_mark = "✓" if gt_l0 == pipe_l0 else "✗"

        lines.append(f"## {rid}")
        lines.append("")

        # L0
        lines.append(f"### L0 {l0_mark}")
        lines.append("")
        l0_desc = l0_rec.get("L0_description", "")
        lines.append(f"- **Pipeline:** `{pipe_l0}` — {l0_desc}")
        lines.append(f"- **Ground truth:** `{gt_l0}`")
        lines.append("")

        # L1
        l1_mark = "✓" if comp_rec.get("L1", {}).get("category_match") else "✗"
        lines.append(f"### L1 {l1_mark}")
        lines.append("")
        lines.append("**Pipeline:**")
        lines.append(fmt_l1_pipeline(l1_rec))
        lines.append("")
        lines.append("**Ground truth:**")
        lines.append(fmt_l1_gt(gt_rec))
        lines.append("")

        # L2
        l2_mark_sub = "✓" if comp_rec.get("L2", {}).get("subcategory_match") else "✗"
        lines.append(f"### L2 {l2_mark_sub}")
        lines.append("")
        lines.append("**Pipeline:**")
        lines.append(fmt_l2_pipeline(l2_rec))
        lines.append("")
        lines.append("**Ground truth:**")
        lines.append(fmt_l2_gt(gt_rec))
        lines.append("")

        lines.append("---")
        lines.append("")

    (READABLE_DIR / "per-record-results.md").write_text("\n".join(lines))

    # -----------------------------------------------------------------------
    # ground-truth.md
    # -----------------------------------------------------------------------
    gt_lines = [
        "# Manual-Subset Ground Truth",
        "",
        f"n={len(ids)} BFL records, manually labelled.",
        "",
        "---",
        "",
    ]
    for rid in ids:
        gt_rec = gt[rid]
        gt_lines.append(f"## {rid}")
        gt_lines.append("")
        gt_lines.append(f"- **L0:** `{gt_rec['L0_classification']}`")
        gt_lines.append(f"- **L1:**")
        gt_lines.append(fmt_l1_gt(gt_rec))
        gt_lines.append(f"- **L2:**")
        gt_lines.append(fmt_l2_gt(gt_rec))
        gt_lines.append("")
        gt_lines.append("---")
        gt_lines.append("")

    (READABLE_DIR / "ground-truth.md").write_text("\n".join(gt_lines))

    # -----------------------------------------------------------------------
    # summary.md
    # -----------------------------------------------------------------------
    l0_match = sum(1 for rid in ids if comp.get(rid, {}).get("L0", {}).get("match"))
    l1_records = [rid for rid in ids if gt[rid]["L0_classification"] == "001HE"]
    l1_match = sum(1 for rid in l1_records if comp.get(rid, {}).get("L1", {}).get("category_match"))
    l2_match_sub = sum(1 for rid in l1_records if comp.get(rid, {}).get("L2", {}).get("subcategory_match"))
    l2_match_cat = sum(1 for rid in l1_records if comp.get(rid, {}).get("L2", {}).get("category_match"))

    def avg(vals):
        return sum(vals) / len(vals) if vals else 0.0

    l1_p = avg([comp[rid]["L1"]["set_metrics"]["precision"] for rid in l1_records])
    l1_r = avg([comp[rid]["L1"]["set_metrics"]["recall"] for rid in l1_records])
    l1_f = avg([comp[rid]["L1"]["set_metrics"]["f1"] for rid in l1_records])
    l2_p = avg([comp[rid]["L2"]["set_metrics_subcategory"]["precision"] for rid in l1_records])
    l2_r = avg([comp[rid]["L2"]["set_metrics_subcategory"]["recall"] for rid in l1_records])
    l2_f = avg([comp[rid]["L2"]["set_metrics_subcategory"]["f1"] for rid in l1_records])

    summary = [
        "# Manual-Subset Pipeline — Summary",
        "",
        "Opus 4.6, temperature 0.3, single run, n=20.",
        "",
        "## L0 (Top-Level)",
        f"- Accuracy: {l0_match}/{len(ids)} ({l0_match/len(ids)*100:.1f}%)",
        "",
        "## L1 (Unsafe Acts, 001HE records only)",
        f"- Records: {len(l1_records)}",
        f"- Exact set match: {l1_match}/{len(l1_records)} ({l1_match/len(l1_records)*100:.1f}%)",
        f"- Set-based macro avg: P={l1_p:.3f}  R={l1_r:.3f}  F1={l1_f:.3f}",
        "",
        "## L2 (Preconditions)",
        f"- Records: {len(l1_records)}",
        f"- Exact subcategory match: {l2_match_sub}/{len(l1_records)} ({l2_match_sub/len(l1_records)*100:.1f}%)",
        f"- Exact parent-category match: {l2_match_cat}/{len(l1_records)} ({l2_match_cat/len(l1_records)*100:.1f}%)",
        f"- Set-based subcategory macro avg: P={l2_p:.3f}  R={l2_r:.3f}  F1={l2_f:.3f}",
        "",
    ]
    (READABLE_DIR / "summary.md").write_text("\n".join(summary))

    print(f"Wrote:")
    print(f"  {READABLE_DIR / 'per-record-results.md'}")
    print(f"  {READABLE_DIR / 'ground-truth.md'}")
    print(f"  {READABLE_DIR / 'summary.md'}")


if __name__ == "__main__":
    main()
