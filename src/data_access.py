import os
import urllib.request

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
SERVICES = ["yellow", "green", "fhvhv"]   
MONTHS = ["2019-06", "2019-07", "2019-08",
          "2024-06", "2024-07", "2024-08",
          "2025-06", "2025-07", "2025-08"]

RAW_DIR = "data/raw"


def raw_path(service, month, raw_dir=RAW_DIR):
    return os.path.join(raw_dir, f"{service}_tripdata_{month}.parquet")

def download_month(service, month, raw_dir=RAW_DIR):
    path = raw_path(service, month, raw_dir)
    if os.path.exists(path):
        return path

    os.makedirs(raw_dir, exist_ok=True)
    url = f"{BASE_URL}/{service}_tripdata_{month}.parquet"
    print("downloading", url)
    urllib.request.urlretrieve(url, path)
    return path

def download_all(months=MONTHS, services=SERVICES):
    for month in months:
        for service in services:
            try:
                download_month(service, month)
            except Exception as error:
                print(f"  could not download {service} {month}: {error}")

if __name__ == "__main__":
    download_all()
