# Notice we’re using pyspark.sql library here
from pyspark.sql import SparkSession

spark = SparkSession.builder \
        .master("local") \
        .appName("CSV file loader") \
        .getOrCreate()

# couple ways of setting configurations
#spark.conf.set("spark.executor.memory", '8g')
#spark.conf.set('spark.executor.cores', '3')
#spark.conf.set('spark.cores.max', '3')
#spark.conf.set("spark.driver.memory", '8g')

file_path = "./AB_NYC_2019.csv"
# Always load csv files with header=True
df = spark.read.csv(file_path, header=True)

df.printSchema()

df.select('neighbourhood').distinct().show(10, False)
