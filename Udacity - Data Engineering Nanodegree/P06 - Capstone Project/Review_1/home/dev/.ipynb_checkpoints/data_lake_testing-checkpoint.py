import pandas as pd
import configparser
from datetime import datetime
import os

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_timestamp, datediff
from pyspark.sql.types import TimestampType, DateType, IntegerType



config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get('CREDENTIALS','AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('CREDENTIALS','AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages","saurfang:spark-sas7bdat:2.0.0-s_2.11,org.apache.hadoop:hadoop-aws:2.7.0")\
        .enableHiveSupport()\
        .getOrCreate()
    return spark



    
def main():
    
    output_data = "s3a://dend-capstone/"
    
    immigration_data = '../../data/18-83510-I94-Data-2016/i94_apr16_sub.sas7bdat'
    temp_data = ''
    airport_data = ''
    demog_data = ''
    
    # start processing
    spark = create_spark_session()
    #df_spark=spark.read.option("mergeSchema", "true").parquet("s3a://dend-capstone/temperature/*/*.parquet")
    #df_spark=spark.read.option("mergeSchema", "true").parquet("s3a://dend-capstone/immigration/*/*/*/*.parquet")
    df_spark=spark.read.parquet("s3a://dend-capstone/us_airports/*.parquet")
    
    df_spark.show(5)
    df_spark.printSchema()
    print(df_spark.count())


if __name__ == "__main__":
    main()