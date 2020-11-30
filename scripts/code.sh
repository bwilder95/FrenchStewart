#!/bin/sh

sleep 10

# Insert in the raw SQL data
if ! mysql -h mysql-container -uroot -ppassword123 -e 'use baseball'; then
  mysql -h mysql-container -uroot -ppassword123 -e "create database baseball;"
  mysql -h mysql-container -uroot -ppassword123 -D baseball < /data/baseball.sql
fi

# Run your scripts
mysql -h mysql-container -uroot -ppassword123 baseball < /scripts/baseball-logic.sql

# Get results
mysql -h mysql-container -uroot -ppassword123 baseball -e '
SELECT a.local_date,a.batter, a.game_id,
    (SELECT SUM(b.Hit)/nullif (SUM(b.atBat),0)
  FROM batting_avg_annual AS b
  WHERE a.game_id=12560 and DATEDIFF(a.local_date,b.local_date) BETWEEN 0 AND 100 and a.batter = b.batter) AS battingavg100day
  FROM batting_avg_annual AS a
  LIMIT 0,20;' > /results/rolling.txt
