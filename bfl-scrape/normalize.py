#!/usr/bin/env python3
"""
Normalize BFL fatalities data.

Currently performs one transformation: in the 'Clothing - Suit' field, the
four skill-prefixed parentheticals are collapsed to (Wingsuit) so the
downstream model sees a single consistent suit label.

  (Expert Wingsuit)        -> (Wingsuit)
  (Unknown Wingsuit)       -> (Wingsuit)
  (Intermediate Wingsuit)  -> (Wingsuit)
  (Beginner Wingsuit)      -> (Wingsuit)

All other fields pass through unchanged. Verification at the end asserts
per-record that every non-Clothing-Suit field is byte-equal to the source
and that every Clothing-Suit change is exactly one of the four literal
substitutions.
"""

import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "bfl_fatalities_unclean.jsonl"
DST = Path(__file__).resolve().parent / "bfl_fatalities.jsonl"

FIELD = "Clothing - Suit"
REPLACEMENTS = [
    ("(Expert Wingsuit)", "(Wingsuit)"),
    ("(Unknown Wingsuit)", "(Wingsuit)"),
    ("(Intermediate Wingsuit)", "(Wingsuit)"),
    ("(Beginner Wingsuit)", "(Wingsuit)"),
]


def normalize_suit(value):
    if not isinstance(value, str):
        return value
    for old, new in REPLACEMENTS:
        value = value.replace(old, new)
    return value


def main():
    with open(SRC) as f:
        src_records = [json.loads(line) for line in f if line.strip()]

    dst_records = []
    for r in src_records:
        out = dict(r)
        if FIELD in out:
            out[FIELD] = normalize_suit(out[FIELD])
        dst_records.append(out)

    # --- verification -------------------------------------------------------
    assert len(src_records) == len(dst_records)

    changed_records = 0
    per_variant = {old: 0 for old, _ in REPLACEMENTS}

    for src, dst in zip(src_records, dst_records):
        # Key sets identical, and every non-FIELD value byte-equal.
        assert src.keys() == dst.keys()
        for k in src:
            if k == FIELD:
                continue
            assert src[k] == dst[k], f"unexpected change in field {k!r}"

        # FIELD change, if any, must be exactly the literal replacements.
        if src.get(FIELD) != dst.get(FIELD):
            changed_records += 1
            expected = src[FIELD]
            for old, new in REPLACEMENTS:
                per_variant[old] += expected.count(old)
                expected = expected.replace(old, new)
            assert dst[FIELD] == expected, (
                f"Clothing - Suit change not explained by known replacements:\n"
                f"  src: {src[FIELD]!r}\n  dst: {dst[FIELD]!r}"
            )

    # Sanity on raw substring counts.
    src_blob = SRC.read_text()
    src_bare = src_blob.count("(Wingsuit)")
    src_variants = {old: src_blob.count(old) for old, _ in REPLACEMENTS}

    assert src_bare == 0, f"unexpected existing (Wingsuit) occurrences in source: {src_bare}"
    for old, n in src_variants.items():
        assert n == per_variant[old], (
            f"per-record count {per_variant[old]} != raw count {n} for {old}"
        )

    # --- write --------------------------------------------------------------
    with open(DST, "w") as f:
        for r in dst_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    dst_blob = DST.read_text()
    dst_bare = dst_blob.count("(Wingsuit)")
    dst_variants = {old: dst_blob.count(old) for old, _ in REPLACEMENTS}

    assert dst_bare == sum(src_variants.values()), (
        f"output (Wingsuit) count {dst_bare} != sum of source variant counts "
        f"{sum(src_variants.values())}"
    )
    for old, n in dst_variants.items():
        assert n == 0, f"output still contains {n} {old}"

    print(f"Records:               {len(src_records)}")
    print(f"Records changed:       {changed_records}")
    for old, n in src_variants.items():
        print(f"  {old:<25} -> (Wingsuit):  {n}")
    print(f"Total (Wingsuit) in output: {dst_bare}")
    print(f"Wrote {DST}")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"VERIFICATION FAILED: {e}", file=sys.stderr)
        sys.exit(1)
