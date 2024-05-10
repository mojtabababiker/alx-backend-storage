-- Rank country origins of band
-- Calculate the number of (non-unique) fans
SELECT DISTINCT origin, SUM(fans) AS nb_fans FROM metal_bands
       GROUP BY origin
       ORDER BY nb_fans DESC;
