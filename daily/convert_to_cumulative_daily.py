"""
Run using:

data:
  timezone_identifier: Asia/Singapore
  delimiter: ","
  decimal: false
  filename: sp_services_import_daily.csv
  datetime_format: "%Y.%m.%d"
  unit_from_entity: false
action: import_statistics.import_from_file

"""
import csv
from datetime import datetime

input_file = "daily_input.csv"
output_file = "sp_services_import_daily.csv"
sensor_id = "sensor:sp_power_energy_import"
unit = "kWh"

cumulative = float(input("Enter the starting Cumulative value: "))

with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=["statistic_id", "unit", "start", "state", "sum"])
    writer.writeheader()

    line_counter = 0
    for row in reader:
        # Remove rows where row["Current"] = '0.0'
        if row["Current"] == '0.0':
            continue
        cumulative += float(row["Current"])
        try:
            writer.writerow(
                {
                    "statistic_id": sensor_id,
                    "unit": unit,
                    "start": datetime.strptime(row["Period"], "%Y-%m-%d").strftime("%Y.%m.%d"),
                    "state": row["Current"],
                    "sum": round(cumulative, 3)
                })
        except Exception as e:
            print(f"Error on line {line_counter}: {row}\n {e}")
        line_counter += 1

    print(f"Cumulative file created with {line_counter} rows")
