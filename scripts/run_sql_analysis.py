import os
import sqlite3
import pandas as pd

# Define paths
csv_path = 'data/processed/delhi_ncr_airbnb_realistic.csv'
db_path = 'airbnb.db'
sql_folder = 'sql'

# Ensure sql directory exists
os.makedirs(sql_folder, exist_ok=True)

# 1. Load realistic dataset
if not os.path.exists(csv_path):
    raise FileNotFoundError(
        f'Could not find {csv_path}. Please complete Phase 2 first.'
    )

df = pd.read_csv(csv_path)

# 2. Connect to SQLite and store as SQL table
conn = sqlite3.connect(db_path)
df.to_sql('listings', conn, if_exists='replace', index=False)
print(' Database "airbnb.db" populated with realistic listings!')

# -------------------------------------------------------------
# SQL QUERY 1: Micro-Market Price Benchmarks (Window Functions)
# -------------------------------------------------------------
sql_benchmark = """
-- Save as sql/01_price_benchmarks.sql
SELECT 
    state,
    neighbourhood,
    area_type,
    COUNT(id) AS total_listings,
    ROUND(AVG(adjusted_price), 2) AS avg_price,
    ROUND(AVG(adjusted_price) - AVG(AVG(adjusted_price)) OVER(PARTITION BY state), 2) AS diff_from_state_avg
FROM listings
GROUP BY state, neighbourhood, area_type
ORDER BY avg_price DESC;
"""

# Save query to .sql file for your GitHub repository
with open(os.path.join(sql_folder, '01_price_benchmarks.sql'), 'w') as f:
  f.write(sql_benchmark)

df_benchmark = pd.read_sql_query(sql_benchmark, conn)
print('\n=== 1. Micro-Market Price Benchmarks (Top 10) ===')
print(df_benchmark.head(10).to_string(index=False))

# -------------------------------------------------------------
# SQL QUERY 2: Superhost vs Regular Host Performance & Pricing
# -------------------------------------------------------------
sql_superhost = """
-- Save as sql/02_superhost_impact.sql
SELECT 
    host_is_superhost,
    COUNT(id) AS property_count,
    ROUND(AVG(adjusted_price), 2) AS avg_price,
    ROUND(AVG(review_scores_rating), 2) AS avg_rating,
    ROUND(AVG(reviews_per_month), 2) AS avg_monthly_demand,
    ROUND(AVG(distance_to_metro_km), 2) AS avg_metro_distance_km
FROM listings
GROUP BY host_is_superhost;
"""

with open(os.path.join(sql_folder, '02_superhost_impact.sql'), 'w') as f:
  f.write(sql_superhost)

df_superhost = pd.read_sql_query(sql_superhost, conn)
print('\n=== 2. Superhost vs Regular Host Impact ===')
print(df_superhost.to_string(index=False))

# -------------------------------------------------------------
# SQL QUERY 3: Price Outliers & Deals (CTE + Z-Score / Quartile logic)
# -------------------------------------------------------------
sql_deals = """
-- Save as sql/03_deal_identifier.sql
WITH NeighborhoodStats AS (
    SELECT 
        neighbourhood,
        AVG(adjusted_price) as avg_neigh_price
    FROM listings
    GROUP BY neighbourhood
)
SELECT 
    l.id,
    l.name,
    l.state,
    l.neighbourhood,
    l.room_type,
    l.adjusted_price,
    ROUND(ns.avg_neigh_price, 2) AS neigh_avg_price,
    ROUND(l.adjusted_price - ns.avg_neigh_price, 2) AS price_variance,
    l.review_scores_rating
FROM listings l
JOIN NeighborhoodStats ns ON l.neighbourhood = ns.neighbourhood
WHERE l.adjusted_price < (ns.avg_neigh_price * 0.75) -- 25% cheaper than neighborhood average
  AND l.review_scores_rating >= 4.5
ORDER BY price_variance ASC;
"""

with open(os.path.join(sql_folder, '03_deal_identifier.sql'), 'w') as f:
  f.write(sql_deals)

df_deals = pd.read_sql_query(sql_deals, conn)
print('\n=== 3. Top High-Rating Bargain Deals (Cheapest vs Local Avg) ===')
print(df_deals.head(5).to_string(index=False))

conn.close()