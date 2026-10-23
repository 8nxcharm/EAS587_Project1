# The Uber Effect: NYC Taxi and Ride-Hailing, 2019 to 2025

EAS 587 Phase 2 project by Aidan Collins and Teslim Carew. We study how NYC's for-hire vehicle market has 
shifted between traditional taxis and ride-hailing, and whether the data supports the claim that Uber has become dominant. 
We use NYC TLC trip records for yellow taxis, green taxis, Uber and Lyft for June to August of 2019, 2024 
and 2025 (27 monthly files), and we compare fares, trip share and airport trips across the two periods.

## How to run

1. Install the packages:
   `pip install -r requirements.txt`
2. From the project root, download and process the data (about 5 minutes):
   `python -m src.pipeline --download`
3. Run the analysis separately: `src/eda.py` for the exploratory analysis and `src/analytics.py` for the first analytics.

## Folders

- `src/`: all code (`data_access.py`, `data_cleaning.py`, `pipeline.py`, `eda.py`, `analytics.py`)
- `data/raw/`: downloaded TLC files
- `data/processed/`: cleaned samples, profile files and `cleaning_log.csv`
- `research_plan.md`: Phase 1 plan
- `phase2_report.md`: Phase 2 report

## Notes

- The random seed is fixed (587), so results repeat.
- The saved files are samples. Use `rows_raw` in `data/processed/cleaning_log.csv` for exact trip counts.
