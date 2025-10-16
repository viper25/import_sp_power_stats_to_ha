# Import Historical Statistics

Export the Daily and hourly statistics from the SP Services dashboard and import them into Home Assistant
using [this](https://github.com/klausj1/homeassistant-statistics?tab=readme-ov-file) Integration. The daily stats seem
to be available for 6 months (inclusive of current running month). The hourly stats seem to be available only for 2
weeks (inclusive of current running week).

After adding from HACS, add the following to `configuration.yaml`

## Steps:

- Download monthly csv data from https://services.spservices.sg/dashboard
- Create a Template Sensor (under Helpers) in Home Assistant (one-time)
  Example:
    ```yaml
    template:
        - sensor:
            - name: "SP Power Energy Import"
              state: "{{ states('sensor.sp_power_energy_import') }}"
              unit_of_measurement: "kWh"
              device_class: energy
              state_class: total_increasing
    ```
- Restart Home Assistant & Set the value of `sensor.sp_power_energy_import` = 0 in Developer Tools > States (one-time).
  It will be 'unknown' initially. This is needed, else the Energy dashboard will complain.
- ~~Now set the static price of electricity
  in [Settings > Energy Dashboard > Grid](http://homeassistant.local/config/energy). This has to be done before
  importing the data else the price will not be retroactively applied.~~
- Make a note of the current cumulative value of the data at http://homeassistant.local/developer-tools/statistics (if not running the first time)
- Run the script to generate say, `convert_to_cumulative_daily.csv`
- Place file in /CONFIG folder in Home Assistant
- Run the script to import the data as below:
    ```yaml
    data:
        timezone_identifier: Asia/Singapore
        delimiter: ","
        decimal: false
        filename: sp_services_import_daily.csv
        datetime_format: "%Y.%m.%d"
        unit_from_entity: false
        action: import_statistics.import_from_file
    ```
- Do the same for hourly data

> One time: Import the sensor in the Energy Dashboard under "Grid". If it shows, no state, then set state to `0` in
> Developer Tools and rerun the above script again.

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

## Reference:

https://chatgpt.com/share/68efa265-dc24-800f-b75f-752123759097