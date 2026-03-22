"""Scrape BASE Fatality List (BFL) from bfl.baseaddict.com into CSV."""

import csv
import html
import json
import re
import sys

import requests

URL = "https://bfl.baseaddict.com/list"
OUTPUT = "bfl_fatalities.csv"

COLUMNS = [
    "BFL entry nr.",
    "Name",
    "Date",
    "Time",
    "Age",
    "Nationality",
    "Location",
    "Category",
    "Object Type",
    "Base seasons",
    "Skydives",
    "WS Skydives",
    "BASE Jumps",
    "WS BASE Jumps",
    "Clothing - Suit",
    "Canopy",
    "Container",
    "Packing & Setup",
    "Weather",
    "Possible Factors",
    "Cause of Death",
    "Accident",
]


def strip_html(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", str(text))
    return html.unescape(text).strip()


def safe(val):
    if val is None:
        return ""
    return str(val).strip()


def combine(*parts, sep=" "):
    return sep.join(p for p in (safe(v) for v in parts) if p)


def transform(rec):
    suit = combine(rec.get("Suit"), f'({rec["SuitType"]})' if rec.get("SuitType") else "")
    canopy_parts = [rec.get("Canopy"), rec.get("CanopyType"), rec.get("CanopyManufacturer")]
    if rec.get("CanopySize"):
        canopy_parts.append(f'{rec["CanopySize"]}')
    canopy = combine(*canopy_parts, sep=", ")

    container = combine(rec.get("Container"), rec.get("ContainerType"), rec.get("ContainerManufacturer"), sep=", ")

    packing = combine(rec.get("Packing"))
    deployment = combine(rec.get("Deployment"))
    packing_setup = ""
    if packing and deployment:
        packing_setup = f"{packing}; Deployment: {deployment}"
    elif packing:
        packing_setup = packing
    elif deployment:
        packing_setup = f"Deployment: {deployment}"

    weather_list = rec.get("Weather") or []
    weather = "; ".join(w.get("Weather", "") for w in weather_list if w.get("Weather"))

    factor_list = rec.get("Factor") or []
    factors = "; ".join(f.get("Factor", "") for f in factor_list if f.get("Factor"))

    area = safe(rec.get("ExitArea"))
    country = safe(rec.get("ExitCountry"))
    location = f"{area}, {country}" if area and country else area or country

    return {
        "BFL entry nr.": safe(rec.get("FormerId")),
        "Name": safe(rec.get("Name")),
        "Date": safe(rec.get("Date")),
        "Time": safe(rec.get("Time")),
        "Age": safe(rec.get("Age")),
        "Nationality": safe(rec.get("Nationality")),
        "Location": location,
        "Category": safe(rec.get("Category")),
        "Object Type": safe(rec.get("ObjectType")),
        "Base seasons": safe(rec.get("Season")),
        "Skydives": safe(rec.get("ExpSkydive")),
        "WS Skydives": safe(rec.get("ExpWsSkydive")),
        "BASE Jumps": safe(rec.get("ExpBASE")),
        "WS BASE Jumps": safe(rec.get("ExpWsBASE")),
        "Clothing - Suit": suit,
        "Canopy": canopy,
        "Container": container,
        "Packing & Setup": packing_setup,
        "Weather": weather,
        "Possible Factors": factors,
        "Cause of Death": safe(rec.get("COD")),
        "Accident": strip_html(rec.get("Description")),
    }


def main():
    print(f"Fetching {URL} ...")
    resp = requests.get(URL, timeout=30, headers={"User-Agent": "ThesisScraper/1.0"})
    resp.raise_for_status()
    html_text = resp.text

    match = re.search(r"var records\s*=\s*", html_text)
    if not match:
        print("ERROR: Could not find 'var records' in page HTML.", file=sys.stderr)
        sys.exit(1)

    decoder = json.JSONDecoder()
    data, _ = decoder.raw_decode(html_text, match.end())

    bfl = data.get("BFL")
    if not bfl:
        print("ERROR: No 'BFL' key found in records.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(bfl)} BFL entries.")

    rows = [transform(rec) for rec in bfl]

    with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
