"""Flatten the L0/L1/L2 classification outputs into a single Excel workbook.

Produces three data sheets plus a README:
    Records         — one row per BFL record (record-level view, n=537)
    L1_acts         — one row per L1 unsafe act       (long format)
    L2_preconditions— one row per L2 precondition     (long format)
    README          — column descriptions

Each data sheet has frozen headers and an autofilter so the workbook is
ready to filter (e.g. L0_classification = "001HE") on open.
"""

import json
import re
from pathlib import Path

import pandas as pd
from openpyxl.utils import get_column_letter

REPO = Path(__file__).resolve().parent.parent
SRC_FILE = REPO / "bfl-scrape" / "bfl_fatalities.jsonl"
OUT_DIR = REPO / "temporary data work"
PIPELINE_OUT = REPO / "classification-pipeline" / "outputs"

L0_FILE = PIPELINE_OUT / "L0_results.jsonl"
L1_FILE = PIPELINE_OUT / "L1_results.jsonl"
L2_FILE = PIPELINE_OUT / "L2_results.jsonl"

WORKBOOK = OUT_DIR / "bfl_classification_workbook.xlsx"


def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


SUIT_RE = re.compile(r"\(([^)]+)\)\s*$")

DISCIPLINE_MAP = {
    "Wingsuit": "wingsuit",
    "Tracking Suit": "tracking",
    "One Piece Tracking Suit": "tracking",
    "Slick": "slick",
}


def derive_discipline(suit_raw, ws_base_jumps):
    """Use the parenthetical category in `Clothing - Suit` as the source of
    truth; fall back to ws_base_jumps>0 only when the suit is missing."""
    if suit_raw:
        m = SUIT_RE.search(suit_raw)
        if m:
            return DISCIPLINE_MAP.get(m.group(1).strip(), "other")
    if ws_base_jumps:
        return "wingsuit"
    return "unknown"


def main():
    src = load_jsonl(SRC_FILE)
    l0 = {r["record_id"]: r for r in load_jsonl(L0_FILE)}
    l1 = {r["record_id"]: r for r in load_jsonl(L1_FILE)}
    l2 = {r["record_id"]: r for r in load_jsonl(L2_FILE)}

    # ----- Records (record-level view) -----
    record_rows = []
    for s in src:
        rid = s["BFL entry nr."]
        l0_rec = l0.get(rid, {})
        l1_rec = l1.get(rid, {})
        l2_rec = l2.get(rid, {})

        l1_acts = l1_rec.get("L1_unsafe_acts") or []
        l2_pcs = l2_rec.get("L2_preconditions") or []

        suit_raw = s.get("Clothing - Suit")
        ws_base = s.get("WS BASE Jumps") or 0
        discipline = derive_discipline(suit_raw, ws_base)

        record_rows.append({
            "record_id": rid,
            "date": s.get("Date"),
            "age": s.get("Age"),
            "nationality": s.get("Nationality"),
            "location": s.get("Location"),
            "object_type": s.get("Object Type"),
            "discipline": discipline,
            "suit_raw": suit_raw,
            "base_seasons": s.get("Base seasons"),
            "base_jumps": s.get("BASE Jumps"),
            "ws_base_jumps": ws_base or None,
            "skydives": s.get("Skydives"),
            "ws_skydives": s.get("WS Skydives"),
            "L0_classification": l0_rec.get("L0_classification"),
            "L0_label": l0_rec.get("L0_label"),
            "L0_description": l0_rec.get("L0_description"),
            "L1_act_count": len(l1_acts),
            "L1_categories": ", ".join(sorted({a.get("category", "") for a in l1_acts})) or None,
            "L2_precondition_count": len(l2_pcs),
            "L2_categories": ", ".join(sorted({p.get("category", "") for p in l2_pcs})) or None,
            "has_error": any("_error" in r for r in (l0_rec, l1_rec, l2_rec) if r),
            "cause_of_death": s.get("Cause of Death"),
            "possible_factors": s.get("Possible Factors"),
            "weather": s.get("Weather"),
            "accident": s.get("Accident"),
        })

    records_df = pd.DataFrame(record_rows)

    # Helper for joining record-level context onto long-format rows
    rid_to_ctx = {
        r["record_id"]: {
            "L0_classification": r["L0_classification"],
            "L0_label": r["L0_label"],
            "discipline": r["discipline"],
            "object_type": r["object_type"],
            "date": r["date"],
        }
        for r in record_rows
    }

    # ----- L1 acts (long format) -----
    l1_rows = []
    for rid, rec in l1.items():
        ctx = rid_to_ctx.get(rid, {})
        for idx, act in enumerate(rec.get("L1_unsafe_acts") or [], start=1):
            l1_rows.append({
                "record_id": rid,
                "act_index": idx,
                "L0_classification": ctx.get("L0_classification"),
                "L0_label": ctx.get("L0_label"),
                "discipline": ctx.get("discipline"),
                "object_type": ctx.get("object_type"),
                "date": ctx.get("date"),
                "L1_category": act.get("category"),
                "L1_label": act.get("label"),
                "L1_description": act.get("description"),
            })
    l1_df = pd.DataFrame(l1_rows)

    # ----- L2 preconditions (long format) -----
    l2_rows = []
    for rid, rec in l2.items():
        ctx = rid_to_ctx.get(rid, {})
        for idx, pc in enumerate(rec.get("L2_preconditions") or [], start=1):
            l2_rows.append({
                "record_id": rid,
                "precondition_index": idx,
                "L0_classification": ctx.get("L0_classification"),
                "L0_label": ctx.get("L0_label"),
                "discipline": ctx.get("discipline"),
                "object_type": ctx.get("object_type"),
                "date": ctx.get("date"),
                "L2_category": pc.get("category"),
                "L2_subcategory": pc.get("subcategory"),
                "L2_label": pc.get("label"),
                "L2_description": pc.get("description"),
                "linked_L1": pc.get("linked_L1"),
            })
    l2_df = pd.DataFrame(l2_rows)

    # ----- README -----
    readme_df = pd.DataFrame([
        ("Records", "One row per BFL record (n=537). Record-level view: source fields, derived discipline, L0 classification, and counts/joined-codes for L1 and L2."),
        ("L1_acts", "One row per L1 unsafe act (n=501 across 424 records). Long format: filter L0_classification or L1_category to read all labels/descriptions in that bucket."),
        ("L2_preconditions", "One row per L2 precondition (n≈462 across ~395 records). Long format: filter L2_category/L2_subcategory to read all labels/descriptions in that bucket."),
        ("", ""),
        ("--- Key columns ---", ""),
        ("discipline", "Derived from `Clothing - Suit` parenthetical. Values: wingsuit / tracking / slick / unknown / other. Falls back to ws_base_jumps>0 only when suit is missing."),
        ("L0_classification", "001HE = human error, 002OC = other cause, 003II = insufficient info."),
        ("L1_category", "101D = decision error, 102S = skill-based error, 103II = insufficient info at L1."),
        ("L2_category", "201C = cognitive/psychological, 202P = physiological/physical, 203T = team/environmental, 204E = equipment. Subcategories carry the C1/C2/C3, P1/P2 detail."),
        ("linked_L1", "On L2 rows: which L1 act category this precondition explains."),
        ("has_error", "On Records sheet: True if any layer returned a parsing/API error for this record."),
    ], columns=["sheet / column", "description"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(WORKBOOK, engine="openpyxl") as xl:
        records_df.to_excel(xl, sheet_name="Records", index=False)
        l1_df.to_excel(xl, sheet_name="L1_acts", index=False)
        l2_df.to_excel(xl, sheet_name="L2_preconditions", index=False)
        readme_df.to_excel(xl, sheet_name="README", index=False)

        # Autofilter, freeze header, set column widths
        for name, df in [
            ("Records", records_df),
            ("L1_acts", l1_df),
            ("L2_preconditions", l2_df),
            ("README", readme_df),
        ]:
            ws = xl.sheets[name]
            ws.freeze_panes = "A2"
            if len(df) > 0:
                ws.auto_filter.ref = ws.dimensions
            for i, col in enumerate(df.columns, start=1):
                sample = [str(v) for v in df[col].head(50).tolist()] + [str(col)]
                width = min(max(len(s) for s in sample) + 2, 60)
                ws.column_dimensions[get_column_letter(i)].width = width

    print(f"Wrote {WORKBOOK}")
    print(f"  Records:           {len(records_df):4d} rows")
    print(f"  L1_acts:           {len(l1_df):4d} rows")
    print(f"  L2_preconditions:  {len(l2_df):4d} rows")
    print()
    print("Discipline distribution:")
    print(records_df["discipline"].value_counts().to_string())
    print()
    print("L0 distribution:")
    print(records_df["L0_classification"].value_counts(dropna=False).to_string())


if __name__ == "__main__":
    main()
