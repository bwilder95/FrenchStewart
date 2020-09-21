-- Show all the available databases
show databases;

-- Use the baseball
use bball;

-- Show all the tables in the baseball database
show tables;

-- Game Table (include limits!)
select *
	from batter_counts
	limit 0,20;

-- Create new table with everyone's hits and atbats
CREATE TABLE batting_avg_hist3
  AS (SELECT batter, atBat, Hit FROM batter_counts)
  
 -- Display table of historic batting percentage for all batters
 select batter, avg(Hit/atBat) as batPercent
 	from batting_avg_hist3 
 	group by batter
 	limit 0,20;

-- Create new table for annual statistics by joining to game_id
create table batting_avg_annual
	as (select batter_counts.batter,batter_counts.Hit,batter_counts.atBat,game.local_date
	from batter_counts 
	inner join game on batter_counts.game_id=game.game_id)
	
 -- Display table of annual average bat percent for each batter
 select batter, avg(Hit/atBat) as batPerrcent,year(local_date) as year
 	from batting_avg_annual
 	group by batter,year
 	limit 0,20;

 -- Create new table for past 100 days batting average
 create table batting_avg_100day
	as (select batter_counts.batter,batter_counts.Hit,batter_counts.atBat,game.local_date
	from batter_counts 
	inner join game on batter_counts.game_id=game.game_id)
	
 -- Display table for past 100 days batting average (March 16,2012 through June 24,2012 (prediction date = June 25,2012))
select batter, avg(Hit/atBat)
	from batting_avg_100day
	where local_date >= '2012-03-16'
	and local_date < '2012-06-24'
	group by batter
 	limit 0,20;
