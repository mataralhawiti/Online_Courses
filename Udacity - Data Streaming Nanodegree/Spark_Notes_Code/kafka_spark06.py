"""
Spark and Kafka Integrating
"""
import logging
from pyspark.sql import SparkSession
import pyspark.sql.functions as psf
from pyspark.sql.types import *

def run_spark_job(spark):

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "policed.epartment.calls03") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", 10) \
        .option("stopGracefullyOnShutdown", "true") \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()

    
    kafka_df = df.selectExpr("CAST(value AS STRING)")

    # we can run this if we don't care about schema and repsrentation
    # query = kafka_df.writeStream.outputMode("append").format("console").start()
    # query.awaitTermination()
    
    # build a schema
    jsonSchema = StructType([
    StructField("crime_id", StringType(), True),
    StructField("original_crime_type_name", StringType(), True),
    StructField("report_date", TimestampType(), True),
    StructField("call_date", TimestampType(), True),
    StructField("offense_date", TimestampType(), True),
    StructField("call_time", StringType(), True),
    StructField("call_date_time", StringType(), True),
    StructField("disposition", StringType(), True),
    StructField("address", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("agency_id", StringType(), True),
    StructField("address_type", StringType(), True),
    StructField("common_location", StringType(), True),
    ])

    # unpack collumns from json "Value"
    json_df =kafka_df\
        .select(psf.from_json(psf.col("value"), jsonSchema).alias("JSON_Topic"))\
        .select("JSON_Topic.*")

    distinct_table = json_df\
        .select('original_crime_type_name','disposition')\
        .distinct()
    
    agg_df = distinct_table\
        .dropna()\
        .select("original_crime_type_name")\
        .groupBy("original_crime_type_name")\
        .agg({'original_crime_type_name':'count'})

    # ready - change name
    query = agg_df.writeStream.outputMode("complete").format("console").start()
    query.awaitTermination()

# ERROR : 'Queries with streaming sources must be executed with writeStream.start();;
 
if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("StructuredStreamingSetup") \
        .getOrCreate()

    logger.info("Spark started")

    run_spark_job(spark)

    spark.stop()

