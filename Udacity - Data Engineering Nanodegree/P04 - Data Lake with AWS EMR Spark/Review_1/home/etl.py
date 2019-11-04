import configparser
from datetime import datetime
import os
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_timestamp
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, dayofweek, date_format, monotonically_increasing_id
from pyspark.sql.types import TimestampType


config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get('CREDENTIALS','AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY']=config.get('CREDENTIALS','AWS_SECRET_ACCESS_KEY')


def create_spark_session():
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    # get filepath to song data file
    song_data = os.path.join(input_data,"song_data/*/*/*/*.json")
    
    # read song data file
    df = spark.read.json(song_data)

    # extract columns to create songs table
    songs_table = df.select(["song_id", "title", "artist_id", "year", "duration"])
    
    # write songs table to parquet files partitioned by year and artist
    songs_table.write.partitionBy("year", "artist_id").parquet(os.path.join(output_data,"songs"), mode="overwrite")

    # extract columns to create artists table
    artists_table = df.select(["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"])
    artists_table = artists_table.withColumnRenamed("artist_name", "name")\
            .withColumnRenamed("artist_location", "location")\
            .withColumnRenamed("artist_latitude", "latitude")\
            .withColumnRenamed("artist_longitude", "longitude")
    
    # write artists table to parquet files
    artists_table.write.parquet(os.path.join(output_data,"artists"), mode="overwrite")


def process_log_data(spark, input_data, output_data):
    # get filepath to log data file
    log_data = os.path.join(input_data,"log_data/*/*/*.json")

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong').dropDuplicates()

    # extract columns for users table    
    users_table = df.select(["userId", "firstName", "lastName", "gender", "level"])\
                .withColumnRenamed("userId", "user_id") \
                .withColumnRenamed("firstName", "first_name") \
                .withColumnRenamed("lastName", "last_name") \
                .dropDuplicates()
    
    # write users table to parquet files
    users_table.write.parquet(os.path.join(output_data,"users"), mode="overwrite")

    # create timestamp column from original timestamp column
    get_timestamp = udf(lambda x: datetime.fromtimestamp(int(x) / 1000), TimestampType())
    df = df.withColumn("hour", hour(get_timestamp(df.ts))) \
            .withColumn("day", dayofmonth(get_timestamp(df.ts))) \
            .withColumn("week", weekofyear(get_timestamp(df.ts))) \
            .withColumn("month", month(get_timestamp(df.ts))) \
            .withColumn("year", year(get_timestamp(df.ts))) \
            .withColumn("weekday", dayofweek(get_timestamp(df.ts))) \
    
    # extract columns to create time table
    time_table = df.select(["ts", "hour", "day", "week", "month", "year", "weekday"]).withColumnRenamed("ts", "start_time")
    
    # write time table to parquet files partitioned by year and month
    time_table.write.partitionBy("year", "month").parquet(os.path.join(output_data,"time"), mode="overwrite")

    # create songplay_id
    df = df.withColumn('songplay_id', monotonically_increasing_id())
    df.createOrReplaceTempView("log_table")
    
    # read in song data to use for songplays table
    song_data = os.path.join(input_data,"song_data/*/*/*/*.json")
    song_df = spark.read.json(song_data)
    song_df.createOrReplaceTempView("songs_table")
    

    # extract columns from joined song and log datasets to create songplays table 
    songplays_table = spark.sql("""
        SELECT  log_table.songplay_id,
                log_table.ts AS start_time,
                log_table.userId AS user_id,
                log_table.level,
                songs_table.song_id AS song_id,
                songs_table.artist_id AS artist_id,
                log_table.sessionId AS session_id,
                log_table.location,
                log_table.userAgent AS user_agen,
                log_table.year,
                log_table.month
        FROM   log_table INNER JOIN songs_table ON log_table.song = songs_table.title AND log_table.artist = songs_table.artist_name AND log_table.length = 
        songs_table.duration
        """)

    # write songplays table to parquet files partitioned by year and month
    songplays_table.write.partitionBy("year", "month").parquet(os.path.join(output_data,"songplays"), mode="overwrite")


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = "s3a://udacity-dend-p04/"
    
#     input_data = "data/"
#     output_data = "data/output/"
    
    #process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)


if __name__ == "__main__":
    main()
