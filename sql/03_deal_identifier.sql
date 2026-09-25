
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
