# Import Historical Statistics

Export the Daily and hourly statistics from the SP Services dashboard and import them into Home Assistant
using [this](https://github.com/klausj1/homeassistant-statistics?tab=readme-ov-file) Integration. The daily stats seem
to be available for 6 months (inclusive of current running month). The hourly stats seem to be available only for 2
weeks (inclusive of current running week).

After adding from HACS, add the following to configuration.yaml

## Steps:

1. Download monthly csv data from https://services.spservices.sg/dashboard
2. Make a note of the current cumulative value of the data at http://homeassistant.local/developer-tools/statistics
3. Run the script to generate import.csv
4. Place contents in /CONFIG folder in Home Assistant
5. Run the script to import the data as below:
    ```yaml
    data:
      timezone_identifier: Asia/Singapore
      delimiter: ","
      decimal: false
      filename: import.tsv
      datetime_format: "%Y.%m.%d"
      unit_from_entity: false
    action: import_statistics.import_from_file
    ```

## Notes

* When running the next time, get the cumulative value from the statistics page and use that as the `cumulative` value
  in the script.
* You can adjust the individual values in the Statistics page to your liking. This can correct any errors due to
  incorrect starting value of `cumulative`. Just correct the value in the Statistics page for the starting date of the
  data set just imported.
* You can reimport the same data multiple times; it will not duplicate the data.

## Sample CSVs

Daily:

```csv
"Period","Current"
"2025-05-01","115.2"
"2025-05-02","55.0"
"2025-05-03","136.1"
"2025-05-04","298.5"
"2025-05-05","56.1"
"2025-05-06","55.2"
```

Hourly:

```csv
"Period","Current"
"2025-10-02 00:00:00","1.9"
"2025-10-02 00:30:00","1.8"
"2025-10-02 01:00:00","1.9"
"2025-10-02 01:30:00","1.6"
"2025-10-02 02:00:00","1.8"
"2025-10-02 02:30:00","1.6"
```