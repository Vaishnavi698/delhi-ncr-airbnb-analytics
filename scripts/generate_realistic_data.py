import os
import numpy as np
import pandas as pd

# Define relative paths
raw_path = 'data/raw/delhi_ncr_airbnb_synthetic.csv'
output_path = 'data/processed/delhi_ncr_airbnb_realistic.csv'

# Ensure output directory exists
os.makedirs('data/processed', exist_ok=True)

# 1. Load raw CSV
if not os.path.exists(raw_path):
    raise FileNotFoundError(
        f'Could not find {raw_path}. Make sure it is inside data/raw/'
    )

df = pd.read_csv(raw_path)

# 2. State Mapping
state_map = {
    'Paharganj': 'Delhi',
    'Lajpat Nagar': 'Delhi',
    'South Extension': 'Delhi',
    'Old Delhi': 'Delhi',
    'Greater Kailash': 'Delhi',
    'Connaught Place': 'Delhi',
    'Janakpuri': 'Delhi',
    'Karol Bagh': 'Delhi',
    'Vasant Kunj': 'Delhi',
    'Hauz Khas': 'Delhi',
    'Dwarka': 'Delhi',
    'Aerocity': 'Delhi',
    'Rajendra Place': 'Delhi',
    'Saket': 'Delhi',
    'Chattarpur': 'Delhi',
    'Mahipalpur': 'Delhi',
    'Defence Colony': 'Delhi',
    'Uttam Nagar': 'Delhi',
    'Vikaspuri': 'Delhi',
    'Mehrauli': 'Delhi',
    'Green Park': 'Delhi',
    'Noida Sector 18': 'Uttar Pradesh',
    'Noida Sector 137': 'Uttar Pradesh',
    'Noida Sector 62': 'Uttar Pradesh',
    'Noida Sector 75': 'Uttar Pradesh',
    'Ghaziabad Indirapuram': 'Uttar Pradesh',
    'Ghaziabad Vaishali': 'Uttar Pradesh',
    'Faridabad Sector 15': 'Haryana',
    'Gurgaon Sector 47': 'Haryana',
    'Gurgaon Golf Course Road': 'Haryana',
    'Gurgaon DLF Phase 2': 'Haryana',
    'Gurgaon Cyber City': 'Haryana',
}
df['state'] = df['neighbourhood'].map(state_map)

# 3. Market Pricing Multipliers by Room Type
multiplier = {
    'Entire home/apt': 1.6,
    'Hotel room': 1.3,
    'Private room': 0.9,
    'Shared room': 0.5,
}

# 4. Realistic Feature Injections
np.random.seed(42)

df['adjusted_price'] = df.apply(
    lambda r: int(r['price'] * multiplier.get(r['room_type'], 1.0)), axis=1
)
df['review_scores_rating'] = np.round(
    np.random.uniform(3.8, 5.0, size=len(df)), 2
)
df['cleanliness_rating'] = np.round(
    np.random.uniform(3.5, 5.0, size=len(df)), 1
)
df['distance_to_metro_km'] = np.round(
    np.random.exponential(scale=1.2, size=len(df)) + 0.2, 2
)
df['amenities_count'] = np.random.randint(5, 25, size=len(df))
df['host_is_superhost'] = np.where(
    (df['review_scores_rating'] >= 4.7) & (df['number_of_reviews'] >= 30),
    't',
    'f',
)
df['instant_bookable'] = np.random.choice(['t', 'f'], size=len(df), p=[0.4, 0.6])

# 5. Save processed CSV
df.to_csv(output_path, index=False)
print(f'Success! Realistic dataset generated at: {output_path}')