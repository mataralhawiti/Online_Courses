"""
Checkpoints
"""
from pyspark.sql import SparkSession

def checkpoint_exercise():
    """
    note that this code will not run in the classroom workspace because we don't have HDFS-compatible file system
    :return:
    """
    spark = SparkSession.builder \
            .master("local") \
            .appName("Checkpoint Example") \
            .getOrCreate()

    df = spark.readStream \
        .format("rate") \
        .option("rowsPerSecond", 90000) \
        .option("rampUpTime", 1) \
        .load()

    rate_raw_data = df.selectExpr("CAST(timestamp AS STRING)", "CAST(value AS string)")

    stream_query = rate_raw_data.writeStream \
        .format("console") \
        .queryName("Default") \
        .option("checkpointLocation", "/tmp/checkpoint") \ #this checkpoint location requires HDFS-like filesystem
        .start()

    # other output option
    #  stream_query = rate_raw_data.writeStream \
    #     .format("parquet") \
    #     .queryName("Default") \
    #     .option("checkpointLocation", "/tmp/checkpoint") \ #this checkpoint location requires HDFS-like filesystem
    #     .start()

if __name__ == "__main__":
    checkpoint_exercise()