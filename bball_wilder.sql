-- Use the baseball
USE baseball;

-- Create new table for annual statistics by joining to game_id
DROP TABLE IF EXISTS batting_avg_annual;
CREATE TABLE batting_avg_annual
	AS (SELECT batter_counts.batter,batter_counts.Hit,batter_counts.atBat,game.local_date
	FROM batter_counts 
	INNER JOIN game ON batter_counts.game_id=game.game_id);
				
 -- Create rolling window table
SELECT a.local_date,a.batter, a.atBat, a.Hit,
(SELECT SUM(b.Hit)/nullif (SUM(b.atBat),0)
FROM batting_avg_annual AS b
WHERE DATEDIFF(a.local_date,b.local_date) BETWEEN 0 AND 100 AND a.batter = b.batter) AS battingavg100day
FROM batting_avg_annual AS a
ORDER BY a.local_date ASC
LIMIT 0,20;
