import argparse
import os
import time

import pandas as pd

from src import data_access
from src.data_cleaning import profile_file, process_file

PROCESSED_DIR = "data/processed"
SAMPLE_FRAC = {"yellow": 0.10, "green": 1.0, "fhvhv": 0.03}
MIN_SAMPLE_ROWS = 250_000


def run(months=data_access.MONTHS, services=data_access.SERVICES,
        raw_dir=data_access.RAW_DIR, out_dir=PROCESSED_DIR):
    os.makedirs(out_dir, exist_ok=True)
    log_rows = []

    for month in months:
        for service in services:
            path = data_access.raw_path(service, month, raw_dir)
            if not os.path.exists(path):
                print(f"[skip] {path} not found")
                continue

            start = time.time()
            try:
                # Profile the raw file: 
                profile, by_vendor, duplicates, memory_all_mb = profile_file(path, service)
                profile.to_csv(f"{out_dir}/profile_{service}_{month}.csv", index=False)
                by_vendor.to_csv(f"{out_dir}/missing_by_vendor_{service}_{month}.csv", index=False)

                # Clean it chunk by chunk and sample
                df, info = process_file(path, service, month, SAMPLE_FRAC[service])

                # Save the processed data
                df.to_parquet(f"{out_dir}/{service}_{month}.parquet", index=False)
            except Exception as error:      # one bad file should not stop the whole run
                print(f"[error] {service} {month}: {error}")
                continue

            info["duplicates_found_in_profile"] = duplicates
            info["est_full_load_all_columns_mb"] = memory_all_mb
            info["seconds"] = round(time.time() - start, 1)
            log_rows.append(info)
            print(f"[done] {service} {month}: {info['rows_raw']:,} raw -> "
                  f"{info['rows_clean']:,} clean -> {info['rows_saved']:,} saved "
                  f"(biggest chunk {info['max_chunk_mb']} MB, whole file would be "
                  f"~{info['est_full_load_mb']} MB, {info['seconds']}s)")
            if SAMPLE_FRAC[service] < 1.0 and info["rows_saved"] < MIN_SAMPLE_ROWS:
                print(f"  WARNING: only {info['rows_saved']:,} rows saved, "
                      f"the handout asks for at least {MIN_SAMPLE_ROWS:,}. Raise SAMPLE_FRAC.")

    log = pd.DataFrame(log_rows)
    if len(log) > 0:
        log.to_csv(f"{out_dir}/cleaning_log.csv", index=False)
    return log


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="download raw files first")
    args = parser.parse_args()

    if args.download:
        data_access.download_all()
    run()