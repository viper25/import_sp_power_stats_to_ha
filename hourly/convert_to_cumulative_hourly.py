"""
Run at http://homeassistant.local/developer-tools/action using:

data:
  timezone_identifier: Asia/Singapore
  delimiter: ","
  decimal: false
  filename: sp_services_import_hourly.csv
  datetime_format: "%Y.%m.%d %H:%M"
  unit_from_entity: false
action: import_statistics.import_from_file

"""

import csv
from datetime import datetime
from collections import defaultdict

input_file = "hourly_input.csv"
output_file = "sp_services_import_hourly.csv"
sensor_id = "sensor.sp_power_energy_import"
unit = "kWh"

cumulative = float(input("Enter the starting Cumulative value: "))

# Collect half-hour rows, aggregate it to hourly
# We keep sum of Current values per hour (ignoring zeros) and also maintain earliest timestamp for formatting
hourly_buckets = defaultdict(float)
# Track whether we saw any non-zero entry in that hour (for potential filtering logic later if needed)
non_zero_seen = set()

rows_parsed = 0
with open(input_file, "r") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        rows_parsed += 1
        current_val_str = row.get("Current")
        if current_val_str is None:
            # Skip if malformed row
            continue
        if current_val_str == '0.0':
            continue  # ignore zero half-hours entirely
        try:
            current_val = float(current_val_str)
        except ValueError:
            continue  # skip invalid numeric values
        try:
            dt = datetime.strptime(row["Period"], "%Y-%m-%d %H:%M:%S")
        except Exception:
            # If timestamp format unexpected, skip
            continue
        hour_dt = dt.replace(minute=0, second=0, microsecond=0)
        hourly_buckets[hour_dt] += current_val
        if current_val != 0.0:
            non_zero_seen.add(hour_dt)

# Write aggregated hourly output rows sorted by hour
with open(output_file, "w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=["statistic_id", "unit", "start", "state", "sum"])
    writer.writeheader()

    hour_counter = 0
    for hour_dt in sorted(hourly_buckets.keys()):
        state_val = hourly_buckets[hour_dt]
        # Skip hour if after aggregation the value is zero (all zeros skipped already, so likely unnecessary)
        if state_val == 0:
            continue
        cumulative = round(cumulative + state_val, 3)
        writer.writerow(
            {
                "statistic_id": sensor_id,
                "unit": unit,
                "start": hour_dt.strftime("%Y.%m.%d %H:%M"),
                "state": round(state_val, 3),
                "sum": cumulative,
            }
        )
        hour_counter += 1

print(f"Aggregated {rows_parsed} input rows into {hour_counter} hourly rows -> {output_file}")
