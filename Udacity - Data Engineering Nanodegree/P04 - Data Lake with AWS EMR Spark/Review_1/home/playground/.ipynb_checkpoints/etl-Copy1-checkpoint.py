import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get('CREDENTIALS','AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('CREDENTIALS','AWS_SECRET_ACCESS_KEY')

# os.environ['AWS_ACCESS_KEY_ID']=config['AWS_ACCESS_KEY_ID']
# os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS_SECRET_ACCESS_KEY']

def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark

def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = input_data
    
    
    # read song data file
    df = spark.read.json(song_data)
    
    print(df.show(5))

#     # extract columns to create songs table
#     songs_table = 
    
#     # write songs table to parquet files partitioned by year and artist
#     songs_table

#     # extract columns to create artists table
#     artists_table = 
    
#     # write artists table to parquet files
#     artists_table
    

def main():
    spark = create_spark_session()
#     for s in spark.sparkContext.getConf().getAll():
#         print(s)
    
    input_data = "s3a://udacity-dend/song_data/A/A/A/TRAAAAK128F9318786.json"
    output_data = "s3a://udacity-dend-p04/"
    
    process_song_data(spark, input_data, output_data)  

if __name__ == "__main__":
    main()
