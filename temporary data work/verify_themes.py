"""Phase 1 — read-only verification of consolidated themes.

Lists distinct L0/L1/L2 label values per HFACS category, with counts, so
typos and near-duplicates ('Late deployment ' vs 'Late deployment') stand
out before we build indicator columns from them.

Reads only — never writes — the consolidated workbook.
"""

from collections import Counter
from pathlib import Path

import openpyxl

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "label-consolidation" / "bfl-classification-consolidated.xlsx"


def rows_as_dicts(ws):
    rows = ws.iter_rows(values_only=True)
    headers = list(next(rows))
    for row in rows:
        yield dict(zip(headers, row))


def report(layer, by_category):
    print(f"\n=== {layer} themes by category ===")
    total_distinct = 0
    total_rows = 0
    for cat, counter in sorted(by_category.items(), key=lambda kv: (kv[0] is None, kv[0])):
        rows = sum(counter.values())
        distinct = len(counter)
        total_distinct += distinct
        total_rows += rows
        print(f"\n  {cat or '<blank>'}  ({distinct} themes, {rows} rows):")
        for label, c in sorted(counter.items(), key=lambda kv: (-kv[1], str(kv[0]))):
            display = repr(label) if (label is None or (isinstance(label, str) and (label != label.strip() or label == ""))) else label
            print(f"    {c:4d}  {display}")
    print(f"\n  {layer} totals: {total_distinct} distinct themes across {total_rows} rows")
    return total_distinct


def main():
    wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)

    # L0 — labels live on the Records sheet
    l0 = Counter()
    for r in rows_as_dicts(wb["Records"]):
        cls = r.get("L0_classification")
        lab = r.get("L0_label")
        if lab is None and cls is None:
            continue
        l0[(cls, lab)] += 1
    by_l0 = {}
    for (cls, lab), c in l0.items():
        by_l0.setdefault(cls, Counter())[lab] = c
    n0 = report("L0", by_l0)

    # L1
    by_l1 = {}
    for r in rows_as_dicts(wb["L1_acts"]):
        cat = r.get("L1_category")
        lab = r.get("L1_label")
        by_l1.setdefault(cat, Counter())[lab] += 1
    n1 = report("L1", by_l1)

    # L2 — group by subcategory if present, else category
    by_l2 = {}
    for r in rows_as_dicts(wb["L2_preconditions"]):
        cat = r.get("L2_subcategory") or r.get("L2_category")
        lab = r.get("L2_label")
        by_l2.setdefault(cat, Counter())[lab] += 1
    n2 = report("L2", by_l2)

    print("\n" + "=" * 60)
    print(f"GRAND TOTAL distinct themes: L0={n0}  L1={n1}  L2={n2}  →  {n0 + n1 + n2}")
    print("=" * 60)

    # Typo proximity check: case-insensitive / whitespace-insensitive matches
    print("\n=== Possible typos (case- or whitespace-only differences) ===")
    found_any = False
    for layer_name, by_cat in [("L0", by_l0), ("L1", by_l1), ("L2", by_l2)]:
        for cat, counter in by_cat.items():
            seen = {}
            for lab in counter:
                if lab is None:
                    continue
                key = lab.strip().lower() if isinstance(lab, str) else lab
                seen.setdefault(key, []).append(lab)
            for key, labs in seen.items():
                if len(labs) > 1:
                    found_any = True
                    print(f"  [{layer_name} / {cat}]  {labs}")
    if not found_any:
        print("  (none)")


if __name__ == "__main__":
    main()
