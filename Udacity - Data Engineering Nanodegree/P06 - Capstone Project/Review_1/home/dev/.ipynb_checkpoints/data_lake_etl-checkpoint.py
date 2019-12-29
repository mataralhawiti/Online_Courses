"""
Python verion NOT Airflow.
Don't used this unless with Airflow.

This is modified version to be run as normal python code in the terminal.
"""
import pandas as pd
import configparser
from datetime import datetime
import os
import json
import logging

# import s3fs
import boto3

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_timestamp, datediff, when, month, year
from pyspark.sql.types import TimestampType, DateType, IntegerType, DoubleType


config = configparser.ConfigParser()
config.read('/home/workspace/airflow/plugins/helpers/dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config.get("CREDENTIALS","AWS_ACCESS_KEY_ID")
os.environ['AWS_SECRET_ACCESS_KEY']=config.get("CREDENTIALS","AWS_SECRET_ACCESS_KEY")

log = logging.getLogger("my-logger")


# spark code
def create_spark_session():
    """ create a spark session
    
    parameters:
        None
    
    Returns:
        spark(spark object): spark seesion
    
    """
    conf = SparkConf().setAll([("spark.jars.packages","saurfang:spark-sas7bdat:2.0.0-s_2.11,org.apache.hadoop:hadoop-aws:2.7.0"), \
                               ("spark.sql.shuffle.partitions", u"10")])
    spark = SparkSession \
        .builder \
        .config(conf=conf)\
        .enableHiveSupport()\
        .getOrCreate()
    log.info('SparkSession was created')
    return spark


# immigration data
def process_immigration(spark, input_data, data_file, output_data):
    """ process immigration raw data, then load into S3 bucket in Parquet format
    
    parameters:
        input(str): S3 bucket path for raw data
        output(atr): S3 bucket path to save the processed data
    
    Returns:
        None
        
    """
    log.info('process_immigrationOperator started')
    
    # load SAS data into spark df with the desired columns
    df_spark = spark.read.parquet(os.path.join(input_data, data_file))

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
    s3 = boto3.resource('s3')
    us_states = list(json.load(s3.Object('dend-capstone-raw', 'I94addr.json').get()['Body']).values())
   
    valid_state = udf(lambda x: '99' if x not in us_states else x)
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
    
    # write spark df to Parquet in S3 bucket
    log.info('write immigration_Parquet to S3 bucket')
    df_spark.write.partitionBy("i94addr","i94yr", "i94mon").parquet(os.path.join(output_data,"immigration"), mode="overwrite")
    

# Tempreture
def process_temperature(spark, input_data, data_file, output_data):
    """ process immigration raw data, then load into S3 bucket in Parquet format
    
    parameters:
        input(str): S3 bucket path for raw data
        output(atr): S3 bucket path to save the processed data
    
    Returns:
        None
        
    """
    log.info('process_temperatureOperator started')
    
    # create spark session
    spark = create_spark_session()
    
    df_spark = spark.read.csv(os.path.join(input_data, data_file) , header = True)
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
    s3 = boto3.resource('s3')
    us_states = json.load(s3.Object('dend-capstone-raw', 'I94addr.json').get()['Body'])
    state_abbr = udf( lambda x: {k.upper(): v.upper() for k, v in us_states.items()}[x.upper()])
    df_spark = df_spark.withColumn("State",  state_abbr(df_spark.State))
    
    # write Parquet file to S3 bucket
    log.info('write temperature_Parquet to S3 bucket')
    df_spark.write.partitionBy("year").parquet(os.path.join(output_data,"temperature"), mode="overwrite")
    
# airports data
def process_airports(spark, input_data, data_file, output_data):
    """ process airports raw data, then load into S3 bucket in Parquet format
    
    parameters:
        input(str): S3 bucket path for raw data
        output(atr): S3 bucket path to save the processed data
    
    Returns:
        None
        
    """
    log.info('process_airportsOperator started')
    
    # create spark session
    spark = create_spark_session()
    
    # load csv to SparkDF
    df_spark = spark.read.format("csv").option("header", "true")\
                                       .option("inferSchema", "true")\
                                       .load(os.path.join(input_data, data_file))
    
    # filter US data only, and required columns
    df_spark = df_spark.filter(df_spark.iso_country == 'US')\
                        .select(['ident', 'type', 'name', 'elevation_ft', 'iso_region', \
                                 'municipality', 'iata_code', 'local_code'])
    
    # substr state code from ISO_REGION, and cast elevation_ft to Int
    df_spark = df_spark.withColumn("iso_region", df_spark.iso_region[-2:2])\
                        .withColumn("elevation_ft", df_spark["elevation_ft"].cast(IntegerType()))
    
    #write to S3 bucket
    log.info('write us_airports_Parquet to S3 bucket')
    df_spark.write.parquet(os.path.join(output_data,"us_airports"), mode="overwrite")


# demographic
def process_us_demographic(spark, input_data, data_file, output_data):
    """ process us demographic  raw data, then load it into S3 bucket in Parquet format
    
    parameters:
        input(str): S3 bucket path for raw data
        output(atr): S3 bucket path to save the processed data
    
    Returns:
        None
        
    """
    log.info('process_us_demographicOperator started')
    
    # create spark session
    spark = create_spark_session()
    
    df_spark = spark.read.csv(os.path.join(input_data, data_file) , sep = ';', header = True)
    
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

    # SQL table, then run query to generate one column per state_Code, groupby State_code
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
    log.info('write us_demographic_Parquet to S3 bucket')
    dem_by_state.write.parquet(os.path.join(output_data,"us_demographic"), mode="overwrite")
    
def copy_to_s3(lookup_files, files_mapping):
    """ copy lookup JSON files from S3 raw data bucket to our data lake S3 bucket
    
    parameters:
        lookup_files(list): list of files that will be copyed to S3
        files_mapping(dict): files names mapping to thier destination in S3
    
    Returns:
        None
        
    """
    log.info('copy_to_s3Operator started')
    
    # S3 client
    s3 = boto3.client('s3')
    
    # copy files from in to out S3 bucket, with approriate names
    log.info('write JSON files to S3 bucket')
    for file in lookup_files:
        copy_source = {'Bucket': 'dend-capstone-raw', 'Key': file}
        s3.copy_object(CopySource=copy_source, Bucket='dend-capstone', Key=files_mapping.get(file, ""))

        
def list_objs_s3():
    """ check if the expteced number of objects were successfully written to our data lake S3
    
    parameters:
        None
    
    Returns:
        None
        
    """
    
    log.info("DataQualityOperator started")
    s3 = boto3.client('s3')
    all_objects = s3.list_objects(Bucket = 'dend-capstone',Delimiter='/')
    
    obj_list = [ obj["Prefix"] for obj in all_objects.get("CommonPrefixes", "") ]
    if len(obj_list) != 8:
        raise ValueError(f"Data quality check failed. We got {len(obj_list)} objects in our S3 data lake, we expect 8")
    else :
        logging.info(f"Data quality on S3 data lake check passed with 8 objects")

def main():
    # S3 buckets
    s3_bucket_in = "s3a://dend-capstone-raw/"
    s3_bucket_out = "s3a://dend-capstone/"

    # data files
    immigration_file = "immigration/*.parquet"
    temperature_file = "GlobalLandTemperaturesByState.csv"
    airports_file = "airport-codes_csv.csv"
    us_demographic_file = "us-cities-demographics.csv"


    lookup_files = ['I94addr.json', 'airlines_iata_codes.json', 'I94port.json', 'I94res.json']
    files_mapping = {'I94addr.json' : 'us_states/us_states.json', 
                    'airlines_iata_codes.json' : 'airlines_iata/airlines_iata.json',
                    'I94port.json' : 'us_ports/us_ports.json',
                    'I94res.json' : 'countries/countries.json'
                    }

    # create spark session
    spark = create_spark_session()

    # start executing
    process_immigration(spark, s3_bucket_in, immigration_file, s3_bucket_out)
    process_temperature(spark, s3_bucket_in, temperature_file, s3_bucket_out)
    process_airports(spark, s3_bucket_in, airports_file, s3_bucket_out)
    process_us_demographic(spark, s3_bucket_in, us_demographic_file, s3_bucket_out)
    

    copy_to_s3(lookup_files, files_mapping)

    list_objs_s3()



if __name__ == "__main__":
    main()