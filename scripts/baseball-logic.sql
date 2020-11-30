DROP TABLE IF EXISTS batting_avg_annual;

CREATE TABLE batting_avg_annual
AS (
    SELECT
            batter_counts.batter
            ,batter_counts.Hit
            ,batter_counts.atBat
            ,game.local_date
            ,batter_counts.game_id
        FROM batter_counts
        INNER JOIN game ON batter_counts.game_id=game.game_id);
