#!/usr/bin/env python3
"""Compare v7 GPT-5.4 run against ground truth. Reads ./output-gpt/, ./ground-truth.jsonl."""

import sys
from pathlib import Path

# Reuse all metric logic from compare_results.py, only swap paths.
import compare_results as base

RUN_DIR = Path(__file__).resolve().parent
base.OUTPUTS_DIR = RUN_DIR / "output-gpt"
base.RESULTS_FILE = base.OUTPUTS_DIR / "classification_results.jsonl"
base.GT_FILE = RUN_DIR / "ground-truth.jsonl"


def patched_main():
    import json, sys as _sys
    if not base.RESULTS_FILE.exists():
        print(f"Error: {base.RESULTS_FILE} not found"); _sys.exit(1)
    if not base.GT_FILE.exists():
        print(f"Error: {base.GT_FILE} not found"); _sys.exit(1)

    gt = base.load_jsonl(base.GT_FILE)
    pipeline = base.load_jsonl(base.RESULTS_FILE)

    comparison = []
    for rid in sorted(gt.keys()):
        gt_rec = gt[rid]
        pipe_rec = pipeline.get(rid)
        if pipe_rec is None:
            print(f"Warning: {rid} missing from pipeline results")
            continue

        entry = {
            "record_id": rid,
            "L0": {
                "gt": gt_rec["L0_classification"],
                "pipeline": pipe_rec.get("L0_classification"),
                "match": gt_rec["L0_classification"] == pipe_rec.get("L0_classification"),
            },
            "L1": {
                "gt_categories": base.extract_l1_categories(gt_rec),
                "pipeline_categories": base.extract_l1_categories(pipe_rec),
                "gt_labels": base.extract_l1_labels(gt_rec),
                "pipeline_labels": base.extract_l1_labels(pipe_rec),
                "category_match": base.sets_match(
                    base.extract_l1_categories(gt_rec),
                    base.extract_l1_categories(pipe_rec)),
                "set_metrics": base.set_precision_recall_f1(
                    base.extract_l1_categories(gt_rec),
                    base.extract_l1_categories(pipe_rec)),
            },
            "L2": {
                "gt_subcategories": base.extract_l2_subcategories(gt_rec),
                "pipeline_subcategories": base.extract_l2_subcategories(pipe_rec),
                "gt_categories": base.extract_l2_categories(gt_rec),
                "pipeline_categories": base.extract_l2_categories(pipe_rec),
                "gt_labels": base.extract_l2_labels(gt_rec),
                "pipeline_labels": base.extract_l2_labels(pipe_rec),
                "subcategory_match": base.sets_match(
                    base.extract_l2_subcategories(gt_rec),
                    base.extract_l2_subcategories(pipe_rec)),
                "category_match": base.sets_match(
                    base.extract_l2_categories(gt_rec),
                    base.extract_l2_categories(pipe_rec)),
                "set_metrics_subcategory": base.set_precision_recall_f1(
                    base.extract_l2_subcategories(gt_rec),
                    base.extract_l2_subcategories(pipe_rec)),
                "set_metrics_category": base.set_precision_recall_f1(
                    base.extract_l2_categories(gt_rec),
                    base.extract_l2_categories(pipe_rec)),
            },
        }
        comparison.append(entry)

    out_path = base.OUTPUTS_DIR / "comparison.jsonl"
    with open(out_path, "w") as f:
        for entry in comparison:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n{'='*70}")
    print(f"  Comparison: v7 GPT-5.4 vs ground truth ({len(comparison)} records)")
    print(f"{'='*70}\n")

    l0_correct = sum(1 for e in comparison if e["L0"]["match"])
    print("--- L0 (Top-Level Classification) ---")
    print(f"Accuracy: {l0_correct}/{len(comparison)} ({l0_correct/len(comparison)*100:.1f}%)\n")

    l0_classes = ["001HE", "002OC", "003II"]
    print(f"{'':>12s}  " + "  ".join(f"{c:>6s}" for c in l0_classes) + "  (predicted)")
    for gt_class in l0_classes:
        row = []
        for pred_class in l0_classes:
            cnt = sum(1 for e in comparison
                      if e["L0"]["gt"] == gt_class and e["L0"]["pipeline"] == pred_class)
            row.append(cnt)
        print(f"{gt_class:>12s}  " + "  ".join(f"{c:>6d}" for c in row))
    print(f"{'(actual)':>12s}\n")

    for cls in l0_classes:
        tp = sum(1 for e in comparison if e["L0"]["gt"] == cls and e["L0"]["pipeline"] == cls)
        fp = sum(1 for e in comparison if e["L0"]["gt"] != cls and e["L0"]["pipeline"] == cls)
        fn = sum(1 for e in comparison if e["L0"]["gt"] == cls and e["L0"]["pipeline"] != cls)
        p = tp / (tp + fp) if (tp + fp) > 0 else 0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0
        print(f"  {cls}: P={p:.3f}  R={r:.3f}  F1={f1:.3f}  (TP={tp} FP={fp} FN={fn})")

    l1_records = [e for e in comparison if e["L0"]["gt"] == "001HE"]
    l1_cat_match = sum(1 for e in l1_records if e["L1"]["category_match"])
    print(f"\n--- L1 (Unsafe Acts — {len(l1_records)} 001HE records) ---")
    if l1_records:
        print(f"Category exact match: {l1_cat_match}/{len(l1_records)} ({l1_cat_match/len(l1_records)*100:.1f}%)")
        l1_p = [e["L1"]["set_metrics"]["precision"] for e in l1_records]
        l1_r = [e["L1"]["set_metrics"]["recall"] for e in l1_records]
        l1_f = [e["L1"]["set_metrics"]["f1"] for e in l1_records]
        print(f"Set-based (macro avg): P={sum(l1_p)/len(l1_p):.3f}  R={sum(l1_r)/len(l1_r):.3f}  F1={sum(l1_f)/len(l1_f):.3f}")

    print()
    for cls in ["101D", "102S", base.L1_INSUFFICIENT_CATEGORY]:
        tp = sum(1 for e in l1_records
                 if e["L1"]["gt_categories"] and cls in e["L1"]["gt_categories"]
                 and e["L1"]["pipeline_categories"] and cls in e["L1"]["pipeline_categories"])
        fp = sum(1 for e in l1_records
                 if (not e["L1"]["gt_categories"] or cls not in e["L1"]["gt_categories"])
                 and e["L1"]["pipeline_categories"] and cls in e["L1"]["pipeline_categories"])
        fn = sum(1 for e in l1_records
                 if e["L1"]["gt_categories"] and cls in e["L1"]["gt_categories"]
                 and (not e["L1"]["pipeline_categories"] or cls not in e["L1"]["pipeline_categories"]))
        p = tp / (tp + fp) if (tp + fp) > 0 else 0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0
        print(f"  {cls}: P={p:.3f}  R={r:.3f}  F1={f1:.3f}  (TP={tp} FP={fp} FN={fn})")

    l1_mismatches = [e for e in l1_records if not e["L1"]["category_match"]]
    if l1_mismatches:
        print("\nL1 mismatches:")
        for e in l1_mismatches:
            print(f"  {e['record_id']}: GT={e['L1']['gt_categories']}  Pipeline={e['L1']['pipeline_categories']}")

    l2_records = [e for e in l1_records
                  if e["L1"]["gt_categories"] is not None and len(e["L1"]["gt_categories"]) > 0]
    l2_sub_match = sum(1 for e in l2_records if e["L2"]["subcategory_match"])
    l2_cat_match = sum(1 for e in l2_records if e["L2"]["category_match"])
    print(f"\n--- L2 (Preconditions — {len(l2_records)} records) ---")
    if l2_records:
        print(f"Category exact match: {l2_cat_match}/{len(l2_records)} ({l2_cat_match/len(l2_records)*100:.1f}%)")
        print(f"Subcategory exact match: {l2_sub_match}/{len(l2_records)} ({l2_sub_match/len(l2_records)*100:.1f}%)")
        l2_p = [e["L2"]["set_metrics_subcategory"]["precision"] for e in l2_records]
        l2_r = [e["L2"]["set_metrics_subcategory"]["recall"] for e in l2_records]
        l2_f = [e["L2"]["set_metrics_subcategory"]["f1"] for e in l2_records]
        print(f"Set-based subcategory (macro avg): P={sum(l2_p)/len(l2_p):.3f}  R={sum(l2_r)/len(l2_r):.3f}  F1={sum(l2_f)/len(l2_f):.3f}")

        mm = [e for e in l2_records if not e["L2"]["subcategory_match"]]
        if mm:
            print("\nL2 subcategory mismatches:")
            for e in mm:
                print(f"  {e['record_id']}: GT={e['L2']['gt_subcategories']}  Pipeline={e['L2']['pipeline_subcategories']}")

    print(f"\nComparison written to: {out_path}")


if __name__ == "__main__":
    patched_main()
