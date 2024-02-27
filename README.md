# transfers
SELECT ratings.rating_value, COALESCE(COUNT(t.Original_risk_rating), 0) AS count_of_ratings
FROM (
    SELECT 'Critical' AS rating_value
    UNION ALL
    SELECT 'Medium'
    UNION ALL
    SELECT 'High'
    UNION ALL
    SELECT 'Low'
) AS ratings
LEFT JOIN your_table_name t ON ratings.rating_value = t.Original_risk_rating
GROUP BY ratings.rating_value;
