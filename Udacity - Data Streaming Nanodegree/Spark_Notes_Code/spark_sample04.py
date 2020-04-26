"""
Structured Streaming
"""
from pyspark.sql import SparkSession
import pyspark.sql.functions as psf
from pyspark.sql.types import *
import logging
import time

spark = SparkSession.builder \
        .master("local") \
        .appName("SparkStreaming Consloe") \
        .getOrCreate()

logging.info("started to listen to the host ..")

jsonSchema = StructType(
    [
        StructField("status", StringType(), True),
        StructField("timestamp", TimestampType(), True)
    ]
)


lines = spark.readStream\
    .option("header", "true")\
    .schema(jsonSchema)\
    .json("/mnt/c/Users/user/udacity_spark/json/")

lines.filter(" status == 'Processed' ")

query = lines.writeStream.outputMode("append").format("console").start()
#query = lines.writeStream.format("console").outputMode("append").start()
time.sleep(2)
query.awaitTermination()