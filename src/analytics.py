import os
import glob
import pandas as pd

print("Calculating Task 3 Analytics Results...\n")


log_df = pd.read_csv("data/processed/cleaning_log.csv")
log_df['year'] = log_df['month'].str[:4]

market_share = log_df.groupby(['year', 'service'])['rows_raw'].sum().unstack().fillna(0)
market_share_pct = (market_share.div(market_share.sum(axis=1), axis=0) * 100).round(2)

print("--- Analytics Result 1: Market Share Shifts (%) ---")
print(market_share_pct)
print("\nNote: August 2019 Uber totals use raw counts to include 2.3M $0-fare trips.")


analytics_results = []
for file in glob.glob("data/processed/*.parquet"):
    temp_df = pd.read_parquet(file, columns=['service', 'fare', 'distance', 'fare_per_mile'])
    service = temp_df['service'].iloc[0]
    year = os.path.basename(file).split('_')[1][:4]
    
    analytics_results.append({
        'Year': year,
        'Service': service,
        'Median_Fare': temp_df['fare'].median(),
        'Median_Distance': temp_df['distance'].median(),
        'Median_Fare_Per_Mile': temp_df['fare_per_mile'].median()
    })

analytics_df = pd.DataFrame(analytics_results).groupby(['Year', 'Service']).mean().round(2)
print("\n--- Analytics Result 2: Pricing and Distance Comparisons ---")
print(analytics_df)
print("\nProcessing complete.")