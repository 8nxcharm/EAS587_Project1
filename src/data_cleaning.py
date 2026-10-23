import pandas as pd
import pyarrow.parquet as pq

SEED = 587                      
CHUNK_SIZE = 1_000_000          
AIRPORT_ZONES = [1, 132, 138]   # EWR, JFK, LaGuardia

COLUMN_MAP = {
    "yellow": {
        "tpep_pickup_datetime": "pickup_time", "tpep_dropoff_datetime": "dropoff_time",
        "PULocationID": "pu_zone", "DOLocationID": "do_zone",
        "trip_distance": "distance", "fare_amount": "fare",
    },
    "green": {
        "lpep_pickup_datetime": "pickup_time", "lpep_dropoff_datetime": "dropoff_time",
        "PULocationID": "pu_zone", "DOLocationID": "do_zone",
        "trip_distance": "distance", "fare_amount": "fare",
    },
    "fhvhv": {
        "hvfhs_license_num": "license", "pickup_datetime": "pickup_time",
        "dropoff_datetime": "dropoff_time", "PULocationID": "pu_zone",
        "DOLocationID": "do_zone", "trip_miles": "distance", "base_passenger_fare": "fare",
    },
}
LICENSE_NAMES = {"HV0003": "Uber", "HV0005": "Lyft"}

# Profiling

def profile_file(path, service):
    rows = 0
    missing = 0
    duplicates = 0
    mins, maxs, pieces = [], [], []

    for batch in pq.ParquetFile(path).iter_batches(batch_size=CHUNK_SIZE):
        df = batch.to_pandas()
        rows += len(df)
        missing = missing + df.isna().sum()
        duplicates += int(df.duplicated(subset=list(COLUMN_MAP[service])).sum())

        numbers = df.select_dtypes(include=["number", "datetime"])   # min and max of these
        mins.append(numbers.min())
        maxs.append(numbers.max())
        pieces.append(df.sample(frac=0.01, random_state=SEED))       # keep 1% of the chunk

    sample = pd.concat(pieces, ignore_index=True)

    profile = pd.DataFrame({                                        # one row per column
        "dtype": sample.dtypes.astype(str),
        "total_rows": rows,
        "n_unique_in_sample": sample.nunique(),
        "pct_missing": (missing / rows * 100).round(2),
        "min": pd.concat(mins, axis=1).apply(lambda row: row.min(), axis=1),
        "max": pd.concat(maxs, axis=1).apply(lambda row: row.max(), axis=1),
    })
    quartiles = sample.quantile([0.25, 0.5, 0.75], numeric_only=True).T
    profile["q1"], profile["median"], profile["q3"] = quartiles[0.25], quartiles[0.5], quartiles[0.75]

    def most_common(col):                                                # most common value, only for columns with few values
        if col.nunique() > 20:
            return ""
        top = col.value_counts(normalize=True).head(1)
        return f"{top.index[0]} ({top.iloc[0] * 100:.0f}%)" if len(top) > 0 else ""
    profile["most_common"] = sample.apply(most_common)
    profile = profile[["dtype", "total_rows", "n_unique_in_sample", "pct_missing", "min",
                       "q1", "median", "q3", "max", "most_common"]]
    profile = profile.reindex(sample.columns).rename_axis("column").reset_index()   # keep file order

    vendor = "hvfhs_license_num" if service == "fhvhv" else "VendorID"                          # % missing for each vendor
    by_vendor = sample.drop(columns=vendor).isna().groupby(sample[vendor]).mean() * 100
    by_vendor = by_vendor.loc[:, by_vendor.sum() > 0].round(2)
    by_vendor.insert(0, "n_rows_in_sample", sample[vendor].value_counts())

    memory_mb = sample.memory_usage(deep=True).sum() / 1_000_000 / 0.01             # memory the whole file would need

    return profile, by_vendor.reset_index(), duplicates, round(memory_mb)


# Cleaning

def clean_chunk(df, service, month, removed):
    df = df.rename(columns=COLUMN_MAP[service])                             # same column names for all three services
    df["service"] = service
    if service == "fhvhv":
        code = df["license"].astype(str).str.strip().str.upper()
        df["carrier"] = code.map(LICENSE_NAMES).fillna("Other")
        df = df.drop(columns="license")
    else:
        df["carrier"] = service.capitalize()

    for col in ["pickup_time", "dropoff_time"]:                                         # data types 
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in ["distance", "fare", "pu_zone", "do_zone"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    before = len(df)                                                                                      # missing values
    df = df.dropna(subset=["pickup_time", "dropoff_time", "pu_zone", "do_zone", "distance", "fare"])
    removed["missing_value"] = removed.get("missing_value", 0) + before - len(df)

    start = pd.Timestamp(month + "-01")
    end = start + pd.offsets.MonthBegin(1)
    minutes = lambda d: (d["dropoff_time"] - d["pickup_time"]).dt.total_seconds() / 60
    rules = [
        ("pickup_outside_month", lambda d: (d["pickup_time"] >= start) & (d["pickup_time"] < end)),
        ("dropoff_not_after_pickup", lambda d: d["dropoff_time"] > d["pickup_time"]),
        ("duration_out_of_range", lambda d: minutes(d).between(1, 180)),                         # 1 minute to 3 hours
        ("distance_out_of_range", lambda d: (d["distance"] > 0) & (d["distance"] <= 100)),
        ("fare_out_of_range", lambda d: d["fare"].between(2.5, 500)),                           # a meter starts at $2.50
        ("invalid_zone", lambda d: d["pu_zone"].between(1, 263) & d["do_zone"].between(1, 263)),
        ("duplicate", lambda d: ~d.duplicated()),                                               # only inside one chunk
    ]
    for reason, keep in rules:
        before = len(df)
        df = df[keep(df)]
        removed[reason] = removed.get(reason, 0) + before - len(df)

    df = df.copy()                                                                # new columns
    df["pu_zone"] = df["pu_zone"].astype(int)
    df["do_zone"] = df["do_zone"].astype(int)
    df["duration_min"] = minutes(df)
    df["fare_per_mile"] = df["fare"] / df["distance"]      # compare short and long trips
    df["hour"] = df["pickup_time"].dt.hour                 # hour of the day
    df["airport_trip"] = df["pu_zone"].isin(AIRPORT_ZONES) | df["do_zone"].isin(AIRPORT_ZONES)
    df["month"] = month

    return df[["service", "carrier", "month", "pickup_time", "dropoff_time", "pu_zone",
               "do_zone", "distance", "duration_min", "fare", "fare_per_mile", "hour",
               "airport_trip"]]

# processing in chunks

def process_file(path, service, month, sample_frac=1.0):
    parquet_file = pq.ParquetFile(path)

    wanted = list(COLUMN_MAP[service])
    for col in wanted:
        if col not in parquet_file.schema_arrow.names:
            raise ValueError(f"{path} is missing the column {col}?")

    removed = {}
    pieces = []
    rows_raw = rows_clean = n_chunks = 0
    max_chunk_mb = total_mb = fare_total = 0

    for chunk in parquet_file.iter_batches(batch_size=CHUNK_SIZE, columns=wanted):
        df = chunk.to_pandas()
        rows_raw += len(df)
        n_chunks += 1
        chunk_mb = df.memory_usage(deep=True).sum() / 1_000_000
        max_chunk_mb = max(max_chunk_mb, chunk_mb)
        total_mb += chunk_mb
        df = clean_chunk(df, service, month, removed)
        rows_clean += len(df)              # exact count, before we sample
        fare_total += df["fare"].sum()

        if sample_frac < 1.0:
            df = df.sample(frac=sample_frac, random_state=SEED)
        pieces.append(df)

    result = pd.concat(pieces, ignore_index=True)

    for col in ["service", "carrier", "month"]:
        result[col] = result[col].astype("category")

    info = {
        "service": service, "month": month,
        "rows_raw": rows_raw, "rows_clean": rows_clean, "rows_saved": len(result),
        "sample_frac": sample_frac, "n_chunks": n_chunks,
        "max_chunk_mb": round(max_chunk_mb),
        "est_full_load_mb": round(total_mb),       # memory to load everything at once
        "mean_fare_clean": round(fare_total / rows_clean, 2),
        "mean_fare_sample": round(result["fare"].mean(), 2),
    }
    info.update(removed)
    return result, info
