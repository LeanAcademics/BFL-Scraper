import json, random
from pathlib import Path

src = Path(__file__).parent / "bfl_fatalities.jsonl"
dst = Path(__file__).parent / "bfl_subset_20.jsonl"

records = []
for line in src.read_text().splitlines():
    line = line.strip()
    if not line:
        continue
    try:
        json.loads(line)
    except json.JSONDecodeError:
        continue
    records.append(line)

sample = random.sample(records, 20)
dst.write_text("\n".join(sample) + "\n")
print(f"Wrote {len(sample)} entries to {dst.name}")
