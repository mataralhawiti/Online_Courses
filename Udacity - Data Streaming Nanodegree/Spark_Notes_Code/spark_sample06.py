# local[2] : it's using 2 partitions at the beginning
# local[*] : means local[{Runtime.getRuntime.availableProcessors()}]

from pyspark.sql import SparkSession
spark = SparkSession.builder \
        .config('spark.ui.port', 3000) \
        .master("local[2]") \
        .appName("data exploration") \
        .getOrCreate()

spark.conf.set('spark.executor.memory', '3g')
spark.conf.set('spark.executor.cores', '3g')

df = spark.read.csv('AB_NYC_2019.csv', header=True)
df1 = df.select('neighbourhood', 'price').distinct()
import pyspark.sql.functions
df1.rdd.getNumPartitions()
df1.repartition(10).agg({"price": "max"}).collect()