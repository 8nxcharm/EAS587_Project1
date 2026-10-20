import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("data/processed", exist_ok=True)

# load the processed parquet files
df_yellow = pd.read_parquet("data/processed/yellow_2024-06.parquet")
df_uberlyft = pd.read_parquet("data/processed/fhvhv_2024-06.parquet")
df_combined = pd.concat([df_yellow, df_uberlyft], ignore_index=True)

# 1. distance histogram
plt.figure(figsize=(10, 5))
sns.histplot(df_yellow['distance'], bins=50, log_scale=True, color='gold')
plt.title("Yellow Taxi Trip Distances - June 2024")
plt.xlabel("Distance (Miles)")
plt.ylabel("Count")
plt.savefig("data/processed/eda_univariate.png", bbox_inches='tight')
plt.close()

# 2. fare vs distance hexbin
plt.figure(figsize=(10, 6))
plt.hexbin(df_yellow['distance'], df_yellow['fare'], gridsize=50, bins='log', cmap='YlOrRd')
plt.colorbar(label='log10(count)')
plt.title("Fare vs. Distance (Yellow Taxi)")
plt.xlabel("Distance (Miles)")
plt.ylabel("Fare ($)")
plt.savefig("data/processed/eda_bivariate.png", bbox_inches='tight')
plt.close()

# 3. fare per mile by carrier
plt.figure(figsize=(10, 6))
sns.boxplot(x='carrier', y='fare_per_mile', data=df_combined, showfliers=False)
plt.title("Fare per Mile by Carrier")
plt.xlabel("Carrier")
plt.ylabel("Fare per Mile ($)")
plt.savefig("data/processed/eda_categorical.png", bbox_inches='tight')
plt.close()

print("Saved EDA plots to data/processed/")