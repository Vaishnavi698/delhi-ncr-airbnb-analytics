
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
