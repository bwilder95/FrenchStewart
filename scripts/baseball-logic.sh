#!/bin/bash

# copy baseball.sql database to container
docker cp baseball.sql mysql-container:/baseball.sql

# select baseball_db
echo "**********USE baseball_db**********"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'USE baseball_db'" # pragma: allowlist secret

# upload data (this step take a while)
echo "**********SOURCE baseball.sql**********..... this step takes 10 minutes*******"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'SOURCE baseball.sql'" # pragma: allowlist secret

# select baseball_db
echo "**********USE baseball_db**********"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'USE baseball_db'" # pragma: allowlist secret

# SHOW tables
echo "**********SHOW tables**********"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'SHOW tables'" # pragma: allowlist secret

# Drop table if exist
echo "**********Checking if have to drop table first**********"
docker exec mysql-container mysql --user=root --password=password123 --database=baseball_db -e " 
DROP TABLE IF EXISTS batting_avg_annual;"

# Creating annual batter average table
echo "**********Calculating annual batter average**********"
docker exec mysql-container mysql --user=root --password=password123 --database=baseball_db -e "
CREATE TABLE batting_avg_annual \
AS (SELECT batter_counts.batter,batter_counts.Hit,batter_counts.atBat,game.local_date,batter_counts.game_id  \
FROM batter_counts \
INNER JOIN game ON batter_counts.game_id=game.game_id);"

# Show stats for game 12560
echo "**********PRESENTING STATS FOR GAME 12560**********"
docker exec mysql-container mysql --user=root --password=password123 --database=baseball_db -e "
SELECT a.local_date,a.batter, a.game_id, \
(SELECT SUM(b.Hit)/nullif (SUM(b.atBat),0) \
FROM batting_avg_annual AS b \
WHERE a.game_id=12560 and DATEDIFF(a.local_date,b.local_date) BETWEEN 0 AND 100 and a.batter = b.batter) AS battingavg100day  \
FROM batting_avg_annual AS a \
LIMIT 0,20;"

# Output storage
echo "**********output new table to storage**********"
chmod +x entrypoint.sh
docker exec mysql-container /docker-entrypoint-initdb.d/dump.sql -u root --password=password123 baseball_db > dump.sql