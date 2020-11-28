#!/bin/bash
KEY = "password123" # pragma: allowlist secret
# copy baseball.sql database to container
docker cp baseball.sql mysql-container:/baseball.sql

# select baseball_db
echo "**********USE baseball_db**********"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'USE baseball_db'" # pragma: allowlist secret

# upload data (this step take a while)
echo "**********SOURCE baseball.sql**********..... this step takes about 15 minutes*******"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'SOURCE baseball.sql'" # pragma: allowlist secret

# select baseball_db
echo "**********USE baseball_db**********"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'USE baseball_db'" # pragma: allowlist secret

# SHOW tables
echo "**********SHOW tables**********"
docker exec mysql-container bash -c "mysql --user=root --password=password123 --database=baseball_db -e 'SHOW tables'" # pragma: allowlist secret

# Drop table if exist
echo "**********Checking if have to drop table first**********"
docker exec mysql-container mysql --user=root --password=KEY --database=baseball_db -e " 
DROP TABLE IF EXISTS batting_avg_annual;"

# Creating annual batter average table
echo "**********Calculating annual batter average**********"
docker exec mysql-container mysql --user=root --password=KEY --database=baseball_db -e "
CREATE TABLE batting_avg_annual \
AS (SELECT batter_counts.batter,batter_counts.Hit,batter_counts.atBat,game.local_date  \
FROM batter_counts \
INNER JOIN game ON batter_counts.game_id=game.game_id);"

# Creating annual batter average table
echo "**********output new table to storage**********"
docker exec mysql-container /docker-entrypoint-initdb.d/dump.sql -u root --password=KEY baseball_db > dump.sql

# Showing first 20 rows of Batter average
echo "**********first 20 rows of Annual Batter average**********"
docker exec mysql-container mysql --user=root --password=KEY  --database=baseball_db -e  "
SELECT batter, (SUM(Hit) / SUM(atBat)) AS batPerrcent,year(local_date) AS year \
FROM batting_avg_annual \
GROUP BY batter, year  \
ORDER BY batter ASC \
LIMIT 0,20;" # pragma: allowlist secret