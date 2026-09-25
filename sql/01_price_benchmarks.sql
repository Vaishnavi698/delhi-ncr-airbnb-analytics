
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
