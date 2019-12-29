import pandas as pd
import configparser
from datetime import datetime
import os
import json

import boto3

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_timestamp, datediff, when, month, year
from pyspark.sql.types import TimestampType, DateType, IntegerType, DoubleType



config = configparser.ConfigParser()
config.read('dl.cfg')

aws_key = os.environ['AWS_ACCESS_KEY_ID']=config.get('CREDENTIALS','AWS_ACCESS_KEY_ID')
aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']=config.get('CREDENTIALS','AWS_SECRET_ACCESS_KEY')

# config = pyspark.SparkConf().setAll([('spark.executor.memory', '8g'), ('spark.executor.cores', '3'), ('spark.cores.max', '3'), ('spark.driver.memory','8g')])
# spark = SparkSession.builder.config(conf=conf).getOrCreate()
#"spark.sql.shuffle.partitions", u"10"
# config("spark.jars.packages","saurfang:spark-sas7bdat:2.0.0-s_2.11,org.apache.hadoop:hadoop-aws:2.7.0")

def create_spark_session():
    conf = SparkConf().setAll([("spark.jars.packages","saurfang:spark-sas7bdat:2.0.0-s_2.11,org.apache.hadoop:hadoop-aws:2.7.0"), \
                               ("spark.sql.shuffle.partitions", u"10")])
    spark = SparkSession \
        .builder \
        .config(conf=conf)\
        .enableHiveSupport()\
        .getOrCreate()
    return spark

def create_s3_client():
    client = boto3.client(
    's3',
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret
    )
    return client
    
def process_immigration(spark, input_data, output_data):
    """
    """
    
    # load SAS data into spark df with the desired columns
    df_spark = spark.read.format('com.github.saurfang.sas.spark')\
                    .load(input_data)
    valid_cols = ['cicid', 'i94yr', 'i94mon', 'i94res', 'i94port', 'arrdate',\
                  'i94mode', 'i94addr', 'depdate', 'i94bir', 'i94visa', 'gender',\
                  'airline', 'visatype']
    df_spark = df_spark.select(valid_cols)
    
    # drop all nulls
    df_spark = df_spark.na.drop()
    
    # cast numberic values to Integer
    df_spark = df_spark.withColumn("cicid", df_spark["cicid"].cast(IntegerType())) \
                    .withColumn("i94yr", df_spark["i94yr"].cast(IntegerType())) \
                    .withColumn("i94mon", df_spark["i94mon"].cast(IntegerType())) \
                    .withColumn("i94res", df_spark["i94res"].cast(IntegerType())) \
                    .withColumn("arrdate", df_spark["arrdate"].cast(IntegerType())) \
                    .withColumn("i94mode", df_spark["i94mode"].cast(IntegerType())) \
                    .withColumn("depdate", df_spark["depdate"].cast(IntegerType())) \
                    .withColumn("i94bir", df_spark["i94bir"].cast(IntegerType())) \
                    .withColumn("i94visa", df_spark["i94visa"].cast(IntegerType()))
    

    # spark udf to cleanup SAS date
    sasdate_to_date = udf(lambda x: ( pd.to_timedelta(x, unit='D') + pd.Timestamp('1960-1-1') ).date(), DateType() )
    df_spark = df_spark.withColumn("arrdate", sasdate_to_date(df_spark.arrdate)) \
                    .withColumn("depdate", sasdate_to_date(df_spark.depdate))
    
    # spark udf to cleanup I94addr
    i94addr_df  = pd.read_json('raw_data/I94addr.json', typ='series').to_frame("state").reset_index().rename(columns={"index": "code"})
    valid_state = udf(lambda x: '99' if x not in list(i94addr_df['code']) else x)
    df_spark = df_spark.withColumn("i94addr", valid_state(df_spark.i94addr))
    
    # replace (I94MODE) codes with values
    df_spark = df_spark.withColumn("i94mode",when(df_spark.i94mode == 1, 'Air')\
                               .when(df_spark.i94mode == 2, 'Sea')\
                               .when(df_spark.i94mode == 3, 'Land')\
                               .otherwise('other'))
    
    # replace (I94MODE) codes with values
    df_spark = df_spark.withColumn("i94visa",when(df_spark.i94visa == 1, 'Business')\
                               .when(df_spark.i94visa == 2, 'Pleasure')\
                               .when(df_spark.i94visa == 3, 'Student')\
                               .otherwise('other'))  
    
    # create new column to calculate the stay length
    df_spark = df_spark.withColumn("stay_length", datediff(df_spark.depdate, df_spark.arrdate) )
    
    #
    df_spark.write.partitionBy("i94addr","i94yr", "i94mon").parquet(os.path.join(output_data,"immigration"), mode="overwrite")
    # write spark df to Parquet in S3 bucket
#     try :
#         df_spark.write.partitionBy("i94addr","i94yr", "i94mon").parquet(os.path.join(output_data,"immigration"), mode="overwrite")
#     except :
#         pass


def process_temperature(spark, input_data, output_data):
    df_spark = spark.read.csv('raw_data/GlobalLandTemperaturesByState.csv', header = True)
    df_spark = df_spark.withColumn("dt", df_spark["dt"].cast(DateType()))\
                        .withColumnRenamed("dt", "date")\
                        .withColumn("State",when(df_spark.State == 'Georgia (State)', 'Georgia')\
                                    .otherwise(df_spark.State))
    
    # filter US and 2011 data
    df_spark = df_spark.filter((df_spark.Country == 'United States') &\
                               (df_spark.date >= '2011-01-01')).dropDuplicates()
    
    # only required columns, and create new column for month and year
    df_spark = df_spark.select(['date', 'AverageTemperature', 'State']) \
                            .withColumn("month", month(df_spark["date"])) \
                            .withColumn("year", year(df_spark["date"]))
    
    # replace state name with abbriviation
    with open('raw_data/I94addr.json') as json_file:
        us_states = json.load(json_file)
    
    state_abbr = udf( lambda x: {k.upper(): v.upper() for k, v in us_states.items()}[x.upper()])
    df_spark = df_spark.withColumn("State",  state_abbr(df_spark.State))
    
    # write Parquet file to S3 bucket
    df_spark.write.partitionBy("year").parquet(os.path.join(output_data,"temperature"), mode="overwrite")
    
    
def process_airports(spark, input_data, output_data):
    df_spark = spark.read.csv('raw_data/airport-codes_csv.csv', header = True)
    
    # filter US data only, and required columns
    df_spark = df_spark.filter(df_spark.iso_country == 'US')\
                        .select(['ident', 'type', 'name', 'elevation_ft', 'iso_region', \
                                 'municipality', 'iata_code', 'local_code'])
    
    # substr state code from ISO_REGION, and cast elevation_ft to Int
    df_spark = df_spark.withColumn("iso_region", df_spark.iso_region[-2:2])\
                        .withColumn("elevation_ft", df_spark["elevation_ft"].cast(IntegerType()))
    
    # write to S3 bucket
    df_spark.write.parquet(os.path.join(output_data,"us_airports"), mode="overwrite")
    

def process_us_demographic(spark, input_data, output_data):
    """
    group data by state_code
    """
    df_spark = spark.read.csv('raw_data/us-cities-demographics.csv', sep = ';', header = True)
    
    # clean up and fix columns names
    df_spark = df_spark.withColumnRenamed("Median Age", "Median_Age")\
                    .withColumnRenamed("Male Population", "Male_Population")\
                    .withColumnRenamed("Female Population", "Female_Population")\
                    .withColumnRenamed("Total Population", "Total_Population")\
                    .withColumnRenamed("Foreign-born", "Foreign_born")\
                    .withColumnRenamed("State Code", "State_Code")\
                    .withColumn("Count", df_spark["Count"].cast(IntegerType())) \
                    .select(['City', 'State', 'Median_Age', 'Male_Population',\
                             'Female_Population', 'Total_Population', 'Foreign_born', 'State_Code',\
                             'Race', 'Count'])
    
    # convert to the correct data types
    df_spark = df_spark.withColumn("Median_Age", df_spark["Median_Age"].cast(DoubleType())) \
                    .withColumn("Male_Population", df_spark["Male_Population"].cast(IntegerType())) \
                    .withColumn("Female_Population", df_spark["Female_Population"].cast(IntegerType())) \
                    .withColumn("Total_Population", df_spark["Total_Population"].cast(IntegerType())) \
                    .withColumn("Foreign_born", df_spark["Foreign_born"].cast(IntegerType())) \
                    .withColumn("Count", df_spark["Count"].cast(IntegerType()))

    # pivot df using Race values
    df_spark = df_spark.groupBy(['City', 'State', 'Median_Age', 'Male_Population',\
                             'Female_Population', 'Total_Population', 'Foreign_born', \
                                      'State_Code'])\
                            .pivot("Race")\
                            .sum("Count")

    # column renaming
    df_spark = df_spark.withColumnRenamed("American Indian and Alaska Native", "Native")\
                        .withColumnRenamed("Black or African-American", "Black")\
                        .withColumnRenamed("Hispanic or Latino", "Hispanic")

    # SQL table, then run query to generate one column per state_Code
    df_spark.createOrReplaceTempView("pivot_table")
    
    dem_by_state = spark.sql("""
    SELECT State_Code,
        cast ( avg(Median_Age) as DECIMAL(4,2) ) as age,
        sum(Male_Population) as Male_Population,
        sum(Female_Population) as Female_Population,
        sum(Total_Population) as Total_Population,
        sum(Foreign_born) as Foreign_born,
        sum(Native) as Native,
        sum(Asian) as Asian,
        sum(Black) as Black,
        sum(White) as White
    FROM pivot_table
    GROUP BY State_Code
    """)
    
    # write to S3 bucket
    dem_by_state.write.parquet(os.path.join(output_data,"us_demographic"), mode="overwrite")
    
    
def upload_to_s3(s3_client, s3_bucket,s3_dir, input_data):
    s3_client.upload_file(Bucket=s3_bucket, Key=s3_dir, Filename=input_data)


def main():
    
    s3_bucket = "dend-capstone"
    s3_bucket_path = "s3a://dend-capstone/"
    
    # data location
    immigration_data = '../../data/18-83510-I94-Data-2016/i94_apr16_sub.sas7bdat'
    
    temperature_data = 'raw_data/GlobalLandTemperaturesByState.csv'
    us_demographic_data = 'raw_data/us-cities-demographics.csv'
    #airports_data = 'raw_data/airport-codes_csv.csv'
    airports_data = "s3://dend-capstone/raw_data/airport-codes_csv.csv"
    
    us_states_data = 'raw_data/I94addr.json'
    airlines_data = 'raw_data/airlines_iata_codes.json'
    us_ports_data = 'raw_data/I94port.json'
    countries_data = 'raw_data/I94res.json'
    
    
    
    # start processing
#     print("start Spark session")
#     spark = create_spark_session()
    
#     print("processing immigration data")
#     process_immigration(spark, immigration_data, s3_bucket_path)
    
    # GlobalLandTemperaturesByState
#     print("processing temperature data")
#     process_temperature(spark, temperature_data, s3_bucket_path)

    #Airports
#     print("processing airports data")
#     process_airports(spark, airports_data, s3_bucket_path)

    
#     print("processing us_demography data")
#     process_us_demographic(spark, us_demographic_data, s3_bucket_path)
    
    
    # uploading files to S3 bucket
#     print("start uploading JSON files to S3 bucket")
    s3_client = create_s3_client()
#     upload_to_s3(s3_client, s3_bucket, 'us_states/us_states.json', us_states_data)
#     upload_to_s3(s3_client, s3_bucket, 'airlines_iata/airlines_iata.json', airlines_data)
#     upload_to_s3(s3_client, s3_bucket, 'us_ports/us_ports.json', us_ports_data)
    upload_to_s3(s3_client, s3_bucket, 'countries/countries.json', countries_data)
    
    s3_client.upload_file(Bucket=s3_bucket, Key=s3_dir, Filename=input_data)
    
    # stop Spark

if __name__ == "__main__":
    main()
    #df_spark=spark.read.option("mergeSchema", "true").parquet("s3a://dend-capstone/immigration/*/*/*/*.parquet")