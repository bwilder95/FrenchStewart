# Utilizing Spark in python to use SQL datasets for ML
# Brenton Wilder
# September 28th, 2020

# Import libraries
import sys
import requests
from pyspark import StorageLevel
from pyspark.sql import SparkSession

# Set main
def main():
    # Initialize Spark
    spark = SparkSession.builder.master("local[*]").getOrCreate()
    database = "baseball"
    port = "3307"
    user = "root"
    password = "password123"
    # Load 'batter_counts' table
    batter_counts = spark.read.format("jdbc").options(
        url=f"jdbc:mysql://localhost:{port}/{database}",
        driver="com.mysql.cj.jdbc.Driver",
        dbtable="batter_counts",
        user=user,
        password=password).load()

    # Load 'game' table
    game = spark.read.format("jdbc").options(
        url=f"jdbc:mysql://localhost:{port}/{database}?zeroDateTimeBehavior=convertToNull",
        driver="com.mysql.cj.jdbc.Driver",
        dbtable="game",
        user=user,
        password=password).load()

    # Join tables as "BballCombine"
    BballCombine = game.join(batter_counts, on=['game_id'], how='inner')

    # Assign to temp view
    batter_counts.createOrReplaceTempView("batter_counts")
    batter_counts.persist(StorageLevel.DISK_ONLY)

    game.createOrReplaceTempView("game")
    game.persist(StorageLevel.DISK_ONLY)

    BballCombine.createOrReplaceTempView("BballCombine")
    BballCombine.persist(StorageLevel.DISK_ONLY)

    # Create rolling table
    roll = spark.sql(
        """
        SELECT a.local_date,a.batter,a.atBat,a.Hit,
        (SELECT SUM(b.Hit)/NULLIF(SUM(b.atBat),0)
        FROM BballCombine AS b
        WHERE DATEDIFF(a.local_date,b.local_date) BETWEEN 0 AND 100 AND a.batter=b.batter) AS battingavg100day
        FROM BballCombine AS a
        ORDER BY a.local_date ASC
        """)
    roll.show()

if __name__ == "__main__":
    sys.exit(main())


