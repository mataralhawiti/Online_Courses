# RDD Example
# https://community.spinup.com/t/h7hqh6x/set-python3-default-ubuntu

import os
from pyspark import SparkConf, SparkContext

# SparkContext : is an entry point to Spark app.
# SparkSession : is another entry point was introduced with Spark SQL

# os.environ["PYSPARK_PYTHON"]="/usr/lib/python3.6"

# print(os.environ.get("PSPARK_HOME"))
# # print(os.environ.get("PYSPARK_PYTHON", 'python'))
# exit(1)
conf = SparkConf().setMaster("local").setAppName("RDD Example")
sc = SparkContext(conf=conf)


# different way of setting configurations 
# conf.setMaster('some url')
# conf.set('spark.executor.memory', '2g')
# conf.set('spark.executor.cores', '4')
# conf.set('spark.cores.max', '40')
# conf.set('spark.logConf', True)


# sparkContext.parallelize materializes/converts/distributes data into RDD
rdd = sc.parallelize(
    [
        ('Richard', 22), ('Alfred', 23), ('Loki',4), ('Albert', 12), ('Alfred', 9)
    ]
)


# action
rdd.collect() # [('Richard', 22), ('Alfred', 23), ('Loki', 4), ('Albert', 12), ('Alfred', 9)]


# create 2 different RDDs
left = sc.parallelize([("Richard", 1), ("Alfred", 4)])
right = sc.parallelize([("Richard", 2), ("Alfred", 5)])

joined_rdd = left.join(right)
collected = joined_rdd.collect()
collected
#print(collected)


# ./bin/spark-submit /mnt/c/Users/user/udacity_spark/spark_sample01.py