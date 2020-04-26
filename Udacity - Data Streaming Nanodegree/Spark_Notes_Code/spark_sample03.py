from pyspark.sql import SparkSession
import pyspark.sql.functions as psf
# source : https://stackoverflow.com/questions/40163106/cannot-find-col-function-in-pyspark/40163314
import pathlib



def explore_data():
    spark = SparkSession.builder \
        .master("local") \
        .appName("Explore data") \
        .getOrCreate()

    file_path = "/mnt/c/Users/user/udacity_spark/cities.csv"
    df = spark.read.csv(file_path, header=True)
    df.printSchema()

    # TODO create another dataframe, drop null columns for start_year
    # TODO select start_year and country only and get distinct values
    # TODO sort by start_year ascending
    distinct_df = df.na.drop(subset=['start_year']) \
        .select("start_year", "country") \
        .distinct() \
        .sort(psf.col("start_year").asc())
    
    # show distinct values
    distinct_df.show()




if __name__ == "__main__":
    explore_data()