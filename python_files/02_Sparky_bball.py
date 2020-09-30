# Utilizing Spark in python to use SQL datasets for ML
# Brenton Wilder
# September 28th, 2020

# Import libraries
import sys
import tempfile
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

    #batter_counts.show()
    # Load 'game' table
    game = spark.read.format("jdbc").options(
        url=f"jdbc:mysql://localhost:{port}/{database}?zeroDateTimeBehavior=convertToNull",
        driver="com.mysql.cj.jdbc.Driver",
        dbtable="game",
        user=user,
        password=password).load()

    #game.show()

    # Join tables as "BballCombine"
    BballCombine = game.join(batter_counts, on=['game_id'], how='inner')


if __name__ == "__main__":
    sys.exit(main())


