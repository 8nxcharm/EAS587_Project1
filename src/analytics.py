import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("data/processed", exist_ok=True)

# market share using raw rows to fix the $0 fare issue in 2019
log_df = pd.read_csv("data/processed/cleaning_log.csv")
log_df['year'] = log_df['month'].str[:4]

market_share = log_df.groupby(['year', 'service'])['rows_raw'].sum().unstack().fillna(0)
market_share_pct = (market_share.div(market_share.sum(axis=1), axis=0) * 100).round(2)

print("market share:")
print(market_share_pct)
print("\n")

# line chart for market share
plt.figure(figsize=(8, 5))
market_share_pct.plot(kind='line', marker='o', linewidth=2)
plt.title("Market Share Shifts Over Time")
plt.xlabel("Year")
plt.ylabel("Market Share (%)")
plt.legend(title="Service")
plt.grid(True, linestyle='--', alpha=0.7)
plt.savefig("data/processed/task3_market_share.png", bbox_inches='tight')
plt.close()

# get pricing medians
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

analytics_df = pd.DataFrame(results).groupby(['Year', 'Service']).mean().round(2).reset_index()

print("pricing medians:")
print(analytics_df.pivot(index='Year', columns='Service', values='Median_Fare_Per_Mile'))

# bar chart for pricing
plt.figure(figsize=(8, 5))
sns.barplot(data=analytics_df, x='Year', y='Median_Fare_Per_Mile', hue='Service')
plt.title("Median Fare per Mile by Year and Service")
plt.xlabel("Year")
plt.ylabel("Median Fare ($)")
plt.legend(title="Service")
plt.savefig("data/processed/task3_pricing.png", bbox_inches='tight')
plt.close()

print("plots saved")