"""
Kafka Source Provider

ulimit -Sn 10000
"""
import logging
from pyspark.sql import SparkSession

def run_spark_job(spark):

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "com.udacity.streams.purchases9999") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", 10) \
        .option("stopGracefullyOnShutdown", "true") \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    spark = SparkSession \
        .builder \
        .master("local") \
        .appName("StructuredStreamingSetup") \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()

# to run:
# ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.5 /mnt/c/Users/user/udacity_spark/kafka_spark.py
