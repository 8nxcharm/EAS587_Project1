import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


os.makedirs("data/processed", exist_ok=True)

print("Loading data for Exploratory Data Analysis...")
# Load a sample of processed data for EDA
df_yellow = pd.read_parquet("data/processed/yellow_2024-06.parquet")
df_uberlyft = pd.read_parquet("data/processed/fhvhv_2024-06.parquet")
df_combined = pd.concat([df_yellow, df_uberlyft], ignore_index=True)


plt.figure(figsize=(10, 5))
sns.histplot(df_yellow['distance'], bins=50, log_scale=True, color='gold')
plt.title("Univariate: Yellow Taxi Trip Distances (Log Scale) - June 2024")
plt.xlabel("Distance (Miles, Log Scale)")
plt.ylabel("Count")
plt.savefig("data/processed/eda_univariate.png", bbox_inches='tight')
plt.close()


plt.figure(figsize=(10, 6))
plt.hexbin(df_yellow['distance'], df_yellow['fare'], gridsize=50, bins='log', cmap='YlOrRd')
plt.colorbar(label='log10(count)')
plt.title("Bivariate: Fare vs. Distance (Yellow Taxi, June 2024)")
plt.xlabel("Distance (Miles)")
plt.ylabel("Fare ($)")
plt.savefig("data/processed/eda_bivariate.png", bbox_inches='tight')
plt.close()


plt.figure(figsize=(10, 6))
sns.boxplot(x='carrier', y='fare_per_mile', data=df_combined, showfliers=False)
plt.title("Categorical Breakdown: Fare per Mile by Carrier")
plt.xlabel("Carrier")
plt.ylabel("Fare per Mile ($)")
plt.savefig("data/processed/eda_categorical.png", bbox_inches='tight')
plt.close()

print("-> Task 2 EDA Complete: Saved 3 plots to data/processed/")