"""Add cost columns to a Home Assistant hourly statistics CSV.

This reads an existing cumulative hourly file with columns:
    statistic_id,unit,start,state,sum
and writes a new file with columns:
    statistic_id,unit,start,state,sum,state_cost,sum_cost

state_cost = state * RATE
sum_cost   = sum * RATE


data:
  timezone_identifier: Asia/Singapore
  delimiter: ","
  decimal: false
  filename: sp_services_import_hourly_with_cost.csv
  datetime_format: "%Y.%m.%d %H:%M"
  unit_from_entity: false
action: import_statistics.import_from_file

"""
from __future__ import annotations
import csv
import os
from typing import List

# ================== Configuration Constants ==================
# Input CSV produced by convert_to_cumulative_hourly.py
INPUT_FILE = "../hourly/sp_services_import_hourly.csv"
# Output CSV with added cost columns
OUTPUT_FILE = "sp_services_import_hourly_with_cost.csv"
# Rate multiplier for cost calculations
RATE = 0.2747
# Decimal places for rounding cost values
ROUND_PLACES = 4
# Overwrite output file if it already exists
OVERWRITE = True
# =============================================================


def validate_header(fieldnames: List[str]) -> None:
    required = {"statistic_id", "unit", "start", "state", "sum"}
    missing = required - set(fieldnames)
    if missing:
        raise SystemExit(f"Input file missing required columns: {', '.join(sorted(missing))}")


def format_cost(value: float, places: int) -> float:
    # Return rounded float; using round to avoid scientific notation; cost usually currency-like.
    return round(value, places)


def main() -> None:
    if not os.path.exists(INPUT_FILE):
        raise SystemExit(f"Input file not found: {INPUT_FILE}")
    if os.path.exists(OUTPUT_FILE) and not OVERWRITE:
        raise SystemExit(f"Output file already exists: {OUTPUT_FILE}. Enable OVERWRITE to replace.")

    rows_written = 0
    rows_skipped = 0

    with open(INPUT_FILE, "r", newline="", encoding="utf-8") as infile, \
            open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(infile)
        validate_header(reader.fieldnames or [])

        out_fieldnames = ["statistic_id", "unit", "start", "state", "sum"]
        writer = csv.DictWriter(outfile, fieldnames=out_fieldnames)
        writer.writeheader()

        for line_no, row in enumerate(reader, start=2):  # header is line 1
            state_str = row.get("state", "").strip()
            sum_str = row.get("sum", "").strip()
            try:
                state_val = float(state_str)
                sum_val = float(sum_str)
            except ValueError:
                rows_skipped += 1
                print(f"Skipping line {line_no}: non-numeric state/sum -> state='{state_str}', sum='{sum_str}'")
                continue

            state_cost = format_cost(state_val * RATE, ROUND_PLACES)
            sum_cost = format_cost(sum_val * RATE, ROUND_PLACES)

            writer.writerow({
                "statistic_id": "sensor.sp_power_energy_import_cost",
                "unit": "SGD",
                "start": row["start"],
                "state": state_cost,
                "sum": sum_cost,
            })
            rows_written += 1

    print(f"Wrote {rows_written} rows to {OUTPUT_FILE}. Skipped {rows_skipped} malformed rows. Rate={RATE} Round={ROUND_PLACES}")


if __name__ == "__main__":
    main()
