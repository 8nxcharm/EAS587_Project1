import os
import glob
import pandas as pd


log_df = pd.read_csv("data/processed/cleaning_log.csv")
log_df['year'] = log_df['month'].str[:4]

market_share = log_df.groupby(['year', 'service'])['rows_raw'].sum().unstack().fillna(0)
market_share_pct = (market_share.div(market_share.sum(axis=1), axis=0) * 100).round(2)

print("Market Share (%)")
print(market_share_pct)
print("\n")


results = []
for file in glob.glob("data/processed/*.parquet"):
    df = pd.read_parquet(file, columns=['service', 'fare', 'distance', 'fare_per_mile'])
    service = df['service'].iloc[0]
    year = os.path.basename(file).split('_')[1][:4]
    
    results.append({
        'Year': year,
        'Service': service,
        'Median_Fare': df['fare'].median(),
        'Median_Distance': df['distance'].median(),
        'Median_Fare_Per_Mile': df['fare_per_mile'].median()
    })

analytics_df = pd.DataFrame(results).groupby(['Year', 'Service']).mean().round(2)
print("Pricing and Distance Medians")
print(analytics_df)