import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set visual style
sns.set_theme(style='whitegrid')

csv_path = 'data/processed/delhi_ncr_airbnb_realistic.csv'

# 1. Load data
if not os.path.exists(csv_path):
  raise FileNotFoundError(
      f'Could not find {csv_path}. Make sure Phase 2 is complete!'
  )

df = pd.read_csv(csv_path)
print(f'Dataset successfully loaded! Shape: {df.shape}')

# -------------------------------------------------------------
# Chart 1: Price Distribution Across NCR States
# -------------------------------------------------------------
plt.figure(figsize=(10, 5))
sns.boxplot(x='state', y='adjusted_price', data=df, palette='Set2')
plt.title('Delhi-NCR Airbnb Price Distribution by State', fontsize=14, pad=12)
plt.xlabel('State / Region', fontsize=11)
plt.ylabel('Nightly Price (₹)', fontsize=11)
plt.tight_layout()
plt.show()

# -------------------------------------------------------------
# Chart 2: Distance to Metro vs Price
# -------------------------------------------------------------
plt.figure(figsize=(10, 5))
sns.scatterplot(
    x='distance_to_metro_km',
    y='adjusted_price',
    hue='room_type',
    data=df,
    alpha=0.7,
    palette='viridis',
)
plt.title(
    'Impact of Metro Proximity on Nightly Listing Price', fontsize=14, pad=12
)
plt.xlabel('Distance to Nearest Metro Station (km)', fontsize=11)
plt.ylabel('Nightly Price (₹)', fontsize=11)
plt.tight_layout()
plt.show()