import json
from pathlib import Path

src = Path(__file__).parent / "bfl_subset_20.jsonl"
dst = Path(__file__).parent / "bfl_subset_20.md"

records = [json.loads(l) for l in src.read_text().splitlines() if l.strip()]

out = ["# BFL Subset (20) — Manual Labelling\n"]
for i, r in enumerate(records, 1):
    out.append(f"## {i}. {r.get('BFL entry nr.', '?')} — {r.get('Name', '?')}\n")
    meta = [
        ("Date", r.get("Date")),
        ("Time", r.get("Time")),
        ("Age", r.get("Age")),
        ("Nationality", r.get("Nationality")),
        ("Location", r.get("Location")),
        ("Object Type", r.get("Object Type")),
        ("Base seasons", r.get("Base seasons")),
        ("Skydives", r.get("Skydives")),
        ("WS Skydives", r.get("WS Skydives")),
        ("BASE Jumps", r.get("BASE Jumps")),
        ("WS BASE Jumps", r.get("WS BASE Jumps")),
        ("Clothing - Suit", r.get("Clothing - Suit")),
        ("Canopy", r.get("Canopy")),
        ("Container", r.get("Container")),
        ("Packing & Setup", r.get("Packing & Setup")),
        ("Weather", r.get("Weather")),
        ("Possible Factors", r.get("Possible Factors")),
        ("Cause of Death", r.get("Cause of Death")),
    ]
    for k, v in meta:
        if isinstance(v, list):
            v = ", ".join(v) if v else "—"
        out.append(f"- **{k}:** {v if v not in (None, '') else '—'}")
    out.append("\n**Accident:**\n")
    out.append(f"> {r.get('Accident', '').strip()}\n")
    out.append("### Manual Labels\n")
    out.append("- **L0 (Top-Level):** ")
    out.append("- **L1 (Unsafe Acts):** ")
    out.append("- **L2 (Preconditions):** ")
    out.append("- **Notes:** ")
    out.append("\n---\n")

dst.write_text("\n".join(out))
print(f"Wrote {len(records)} entries to {dst.name}")
