#!/usr/bin/env python3
"""
Compare this run's classification results against the local ground truth.

Reads:  ./output/classification_results.jsonl
        ./ground-truth.jsonl
Writes: ./output/comparison.jsonl
"""

import json
import sys
from pathlib import Path

RUN_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = RUN_DIR / "output"
GT_FILE = RUN_DIR / "ground-truth.jsonl"
RESULTS_FILE = OUTPUTS_DIR / "classification_results.jsonl"

L1_INSUFFICIENT_CATEGORY = "103II"


def load_jsonl(path):
    records = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                records[rec["record_id"]] = rec
    return records


def extract_l1_categories(record):
    acts = record.get("L1_unsafe_acts")
    if acts is None:
        return None
    return sorted(set(a["category"] for a in acts))


def extract_l1_labels(record):
    acts = record.get("L1_unsafe_acts")
    if acts is None:
        return None
    return [f"{a['category']} - {a.get('label', '')}" for a in acts]


def extract_l2_subcategories(record):
    preconds = record.get("L2_preconditions")
    if preconds is None:
        return None
    subs = set()
    for p in preconds:
        sub = p.get("subcategory")
        if sub is None:
            sub = p.get("category")
        if sub is not None:
            subs.add(sub)
    return sorted(subs)


def _parent_category(code):
    if not code:
        return code
    if code.startswith("201C"):
        return "201C"
    if code.startswith("202P"):
        return "202P"
    if code.startswith("203T"):
        return "203T"
    if code.startswith("204E"):
        return "204E"
    return code


def extract_l2_categories(record):
    preconds = record.get("L2_preconditions")
    if preconds is None:
        return None
    cats = set()
    for p in preconds:
        cat = p.get("category")
        sub = p.get("subcategory")
        cats.add(_parent_category(cat) if cat else _parent_category(sub))
    return sorted(c for c in cats if c)


def extract_l2_labels(record):
    preconds = record.get("L2_preconditions")
    if preconds is None:
        return None
    return [
        f"{p.get('subcategory') or p.get('category')}→{p.get('linked_L1', '?')} - {p.get('label', '')}"
        for p in preconds
    ]


def sets_match(gt_set, pipeline_set):
    if gt_set is None and pipeline_set is None:
        return True
    if gt_set is None or pipeline_set is None:
        gt_empty = gt_set is None or len(gt_set) == 0
        pipe_empty = pipeline_set is None or len(pipeline_set) == 0
        return gt_empty and pipe_empty
    return set(gt_set) == set(pipeline_set)


def set_precision_recall_f1(gt_set, pipeline_set):
    if gt_set is None:
        gt_set = []
    if pipeline_set is None:
        pipeline_set = []

    gt = set(gt_set)
    pred = set(pipeline_set)

    if len(pred) == 0 and len(gt) == 0:
        return {"precision": 1.0, "recall": 1.0, "f1": 1.0}
    if len(pred) == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    if len(gt) == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    tp = len(gt & pred)
    precision = tp / len(pred) if pred else 0.0
    recall = tp / len(gt) if gt else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {"precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}


def main():
    if not RESULTS_FILE.exists():
        print(f"Error: {RESULTS_FILE} not found")
        sys.exit(1)
    if not GT_FILE.exists():
        print(f"Error: {GT_FILE} not found")
        sys.exit(1)

    gt = load_jsonl(GT_FILE)
    pipeline = load_jsonl(RESULTS_FILE)

    comparison = []

    for rid in sorted(gt.keys()):
        gt_rec = gt[rid]
        pipe_rec = pipeline.get(rid)

        if pipe_rec is None:
            print(f"Warning: {rid} missing from pipeline results")
            continue

        gt_l0 = gt_rec["L0_classification"]
        pipe_l0 = pipe_rec.get("L0_classification")

        gt_l1_cats = extract_l1_categories(gt_rec)
        pipe_l1_cats = extract_l1_categories(pipe_rec)

        gt_l2_subcats = extract_l2_subcategories(gt_rec)
        pipe_l2_subcats = extract_l2_subcategories(pipe_rec)

        gt_l2_cats = extract_l2_categories(gt_rec)
        pipe_l2_cats = extract_l2_categories(pipe_rec)

        entry = {
            "record_id": rid,
            "L0": {
                "gt": gt_l0,
                "pipeline": pipe_l0,
                "match": gt_l0 == pipe_l0,
            },
            "L1": {
                "gt_categories": gt_l1_cats,
                "pipeline_categories": pipe_l1_cats,
                "gt_labels": extract_l1_labels(gt_rec),
                "pipeline_labels": extract_l1_labels(pipe_rec),
                "category_match": sets_match(gt_l1_cats, pipe_l1_cats),
                "set_metrics": set_precision_recall_f1(gt_l1_cats, pipe_l1_cats),
            },
            "L2": {
                "gt_subcategories": gt_l2_subcats,
                "pipeline_subcategories": pipe_l2_subcats,
                "gt_categories": gt_l2_cats,
                "pipeline_categories": pipe_l2_cats,
                "gt_labels": extract_l2_labels(gt_rec),
                "pipeline_labels": extract_l2_labels(pipe_rec),
                "subcategory_match": sets_match(gt_l2_subcats, pipe_l2_subcats),
                "category_match": sets_match(gt_l2_cats, pipe_l2_cats),
                "set_metrics_subcategory": set_precision_recall_f1(gt_l2_subcats, pipe_l2_subcats),
                "set_metrics_category": set_precision_recall_f1(gt_l2_cats, pipe_l2_cats),
            },
        }
        comparison.append(entry)

    out_path = OUTPUTS_DIR / "comparison.jsonl"
    with open(out_path, "w") as f:
        for entry in comparison:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # -----------------------------------------------------------------------
    # Summary
    # -----------------------------------------------------------------------
    print(f"\n{'='*70}")
    print(f"  Comparison: pipeline vs ground truth ({len(comparison)} records)")
    print(f"{'='*70}\n")

    l0_correct = sum(1 for e in comparison if e["L0"]["match"])
    print(f"--- L0 (Top-Level Classification) ---")
    print(f"Accuracy: {l0_correct}/{len(comparison)} ({l0_correct/len(comparison)*100:.1f}%)\n")

    l0_classes = ["001HE", "002OC", "003II"]
    print(f"{'':>12s}  " + "  ".join(f"{c:>6s}" for c in l0_classes) + "  (predicted)")
    for gt_class in l0_classes:
        row = []
        for pred_class in l0_classes:
            count = sum(1 for e in comparison
                       if e["L0"]["gt"] == gt_class and e["L0"]["pipeline"] == pred_class)
            row.append(count)
        print(f"{gt_class:>12s}  " + "  ".join(f"{c:>6d}" for c in row))
    print(f"{'(actual)':>12s}")

    print()
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

        l1_precisions = [e["L1"]["set_metrics"]["precision"] for e in l1_records]
        l1_recalls = [e["L1"]["set_metrics"]["recall"] for e in l1_records]
        l1_f1s = [e["L1"]["set_metrics"]["f1"] for e in l1_records]
        print(f"Set-based (macro avg): P={sum(l1_precisions)/len(l1_precisions):.3f}  "
              f"R={sum(l1_recalls)/len(l1_recalls):.3f}  "
              f"F1={sum(l1_f1s)/len(l1_f1s):.3f}")

    l1_classes = ["101D", "102S", L1_INSUFFICIENT_CATEGORY]
    print()
    for cls in l1_classes:
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
        print(f"\nL1 mismatches:")
        for e in l1_mismatches:
            print(f"  {e['record_id']}: GT={e['L1']['gt_categories']}  Pipeline={e['L1']['pipeline_categories']}")

    l2_records = [e for e in l1_records
                  if e["L1"]["gt_categories"] is not None and len(e["L1"]["gt_categories"]) > 0]
    l2_sub_match = sum(1 for e in l2_records if e["L2"]["subcategory_match"])
    l2_cat_match = sum(1 for e in l2_records if e["L2"]["category_match"])
    print(f"\n--- L2 (Preconditions — {len(l2_records)} records with L1 acts) ---")
    if l2_records:
        print(f"Category exact match: {l2_cat_match}/{len(l2_records)} ({l2_cat_match/len(l2_records)*100:.1f}%)")
        print(f"Subcategory exact match: {l2_sub_match}/{len(l2_records)} ({l2_sub_match/len(l2_records)*100:.1f}%)")

        l2_precisions = [e["L2"]["set_metrics_subcategory"]["precision"] for e in l2_records]
        l2_recalls = [e["L2"]["set_metrics_subcategory"]["recall"] for e in l2_records]
        l2_f1s = [e["L2"]["set_metrics_subcategory"]["f1"] for e in l2_records]
        print(f"Set-based subcategory (macro avg): P={sum(l2_precisions)/len(l2_precisions):.3f}  "
              f"R={sum(l2_recalls)/len(l2_recalls):.3f}  "
              f"F1={sum(l2_f1s)/len(l2_f1s):.3f}")

        l2_mismatches = [e for e in l2_records if not e["L2"]["subcategory_match"]]
        if l2_mismatches:
            print(f"\nL2 subcategory mismatches:")
            for e in l2_mismatches:
                print(f"  {e['record_id']}: GT={e['L2']['gt_subcategories']}  Pipeline={e['L2']['pipeline_subcategories']}")

    print(f"\nComparison written to: {out_path}")


if __name__ == "__main__":
    main()
