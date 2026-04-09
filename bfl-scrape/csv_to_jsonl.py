"""Convert bfl_fatalities.csv to a clean JSONL file (one JSON object per line).

Multi-value fields (Weather, Possible Factors) are split into arrays.
Numeric fields (Age, Skydives, etc.) are converted to numbers where possible.
Empty strings become null.
"""

import csv
import json

INPUT = "bfl_fatalities.csv"
OUTPUT = "bfl_fatalities.jsonl"

# Fields that contain semicolon-separated lists → convert to arrays
LIST_FIELDS = ["Weather", "Possible Factors"]

# Fields that should be numbers → convert to int
NUMERIC_FIELDS = ["Age", "Base seasons", "Skydives", "WS Skydives", "BASE Jumps", "WS BASE Jumps"]


def clean_value(value):
    """Turn empty strings into None."""
    if value is None or value.strip() == "":
        return None
    return value.strip()


def to_int(value):
    """Try to convert to int, return None if not possible."""
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return value  # keep original string if not a clean number


def split_list(value):
    """Split a semicolon-separated string into a list of trimmed strings."""
    if value is None:
        return []
    return [item.strip() for item in value.split(";") if item.strip()]


def convert_row(row):
    """Convert one CSV row dict into a clean JSON-ready dict."""
    record = {}

    for key, value in row.items():
        record[key] = clean_value(value)

    # Convert list fields from "A; B; C" → ["A", "B", "C"]
    for field in LIST_FIELDS:
        record[field] = split_list(record.get(field))

    # Convert numeric fields to integers
    for field in NUMERIC_FIELDS:
        record[field] = to_int(record.get(field))

    return record


def main():
    with open(INPUT, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [convert_row(row) for row in reader]

    with open(OUTPUT, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Converted {len(rows)} records → {OUTPUT}")


if __name__ == "__main__":
    main()
