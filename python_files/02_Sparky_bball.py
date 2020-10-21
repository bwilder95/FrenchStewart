# Utilizing Spark in python to use SQL datasets for ML
# Brenton Wilder
# September 28th, 2020

# Import libraries
import sys

from pyspark import StorageLevel
from pyspark.sql import SparkSession


# Set main
def main():
    # Initialize Spark
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    database = "baseball"
    port = "3307"
    user = "root"
    password = "password123"  # pragma: allowlist secret
    # Load 'batter_counts' table
    batter_counts = (
        spark.read.format("jdbc")
        .options(
            url=f"jdbc:mysql://localhost:{port}/{database}",
            driver="com.mysql.cj.jdbc.Driver",
            dbtable="batter_counts",
            user=user,
            password=password,
        )
        .load()
    )

    # Load 'game' table
    game = (
        spark.read.format("jdbc")
        .options(
            url=f"jdbc:mysql://localhost:{port}/{database}?zeroDateTimeBehavior=convertToNull",
            driver="com.mysql.cj.jdbc.Driver",
            dbtable="game",
            user=user,
            password=password,
        )
        .load()
    )

    # Assign to temp view
    batter_counts.createOrReplaceTempView("batter_counts")
    batter_counts.persist(StorageLevel.DISK_ONLY)
    game.createOrReplaceTempView("game")
    game.persist(StorageLevel.DISK_ONLY)

    # Create joinTable
    joinTable = spark.sql(
        """
        SELECT batter_counts.batter, batter_counts.Hit, batter_counts.atBat, game.local_date
	    FROM batter_counts 
	    JOIN game ON batter_counts.game_id = game.game_id
        """
    )
    # joinTable.show()
    joinTable.createOrReplaceTempView("joinTable")
    joinTable.persist(StorageLevel.DISK_ONLY)

    # Create rolling window table
    rollTable = spark.sql(
        """
        SELECT a.local_date, SUM(a.Hit)/nullif (SUM(a.atBat),0)
        FROM joinTable as a
        JOIN joinTable as b
        ON a.local_date WHERE DATEDIFF(a.local_date,b.local_date) & 0 AND 100  
            & a.batter=b.batter
        """
    )
    rollTable.show()


if __name__ == "__main__":
    sys.exit(main())
