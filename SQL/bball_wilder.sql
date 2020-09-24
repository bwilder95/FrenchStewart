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

-- Create rolling window table
select a.local_date,a.batter,
round((select avg(b.Hit/b.atBat)
	from batting_avg_annual as b
	where datediff(a.local_date,b.local_date) between 0 and 100
	),7) as '100dayMovingAVG'
	from batting_avg_annual as a
	order by a.batter,a.local_date desc
	limit 0,20;
