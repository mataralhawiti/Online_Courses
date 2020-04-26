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
        .option("subscribe", "com.udacity.streams.purchases9999") \
        .option("startingOffsets", "earliest") \
        .option("maxOffsetsPerTrigger", 10) \
        .option("stopGracefullyOnShutdown", "true") \
        .load()

    # Show schema for the incoming resources for checks
    df.printSchema()
    """
        Once received from Kafka, the source will have the following schema:
        key[binary]
        value[binary]
        topic[string]
        partition[int]
        offset[long]
        timestamp[long]
        timestampType[int]
    """
    
    kafka_df = df.selectExpr("CAST(value AS STRING)")

    # we can run this if we don't care about schema and repsrentation
    # query = kafka_df.writeStream.outputMode("append").format("console").start()
    # query.awaitTermination()
    
    # build a schema
    jsonSchema = StructType(
        [
            StructField("username", StringType(), True),
            StructField("currency", StringType(), True),
            StructField("amount", IntegerType(), True)
        ]
    )

    # unpack collumns from json "Value"
    json_df =kafka_df\
        .select(psf.from_json(psf.col("value"), jsonSchema).alias("JSON_Topic"))\
        .select("JSON_Topic.*")

    query = json_df.writeStream.outputMode("append").format("console").start()
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


"""
########### Spark Console Shows Progress Reports ################33

output in spark logs (remeber spark process batches !!):

-------------------------------------------
Batch: 1
-------------------------------------------
+--------------+--------+------+
|      username|currency|amount|
+--------------+--------+------+
|     anthony16|     QAR|163370|
|        bbrown|     HTG|119779|
|  rickykennedy|     SHP|  1299|
|herringkatelyn|     NIS| 94252|
|    garciajohn|     AFN| 46042|
|      ejackson|     KES| 73290|
|       nbrooks|     NGN| 25518|
|  sallyjohnson|     GYD|176506|
|  valerieramos|     MVR|183489|
|colemanbernard|     BMD|164326|
+--------------+--------+------+

20/04/24 17:03:43 INFO WriteToDataSourceV2Exec: Data source writer org.apache.spark.sql.execution.streaming.sources.MicroBatchWriter@7b8ef34c committed.
20/04/24 17:03:43 INFO SparkContext: Starting job: start at NativeMethodAccessorImpl.java:0
20/04/24 17:03:43 INFO DAGScheduler: Job 3 finished: start at NativeMethodAccessorImpl.java:0, took 0.000036 s
20/04/24 17:03:43 INFO CheckpointFileManager: Writing atomically to file:/tmp/temporary-38a86267-6e7b-431c-8ffb-1779ef953601/commits/1 using temp file file:/tmp/temporary-38a86267-6e7b-431c-8ffb-1779ef953601/commits/.1.6e7b0987-8d23-439c-baaf-ed71d784bd30.tmp
20/04/24 17:03:43 INFO CheckpointFileManager: Renamed temp file file:/tmp/temporary-38a86267-6e7b-431c-8ffb-1779ef953601/commits/.1.6e7b0987-8d23-439c-baaf-ed71d784bd30.tmp to file:/tmp/temporary-38a86267-6e7b-431c-8ffb-1779ef953601/commits/1
20/04/24 17:03:43 INFO MicroBatchExecution: 



########## progress report ##########

Streaming query made progress: {
  "id" : "bc0509cb-9951-4c7c-99af-632368e86d91",
  "runId" : "90873c0d-f9d8-4b02-b611-ae1abe533dfd",
  "name" : null,
  "timestamp" : "2020-04-24T14:03:42.769Z",
  "batchId" : 1,
  "numInputRows" : 10,
  "inputRowsPerSecond" : 2.0157226365652083,
  "processedRowsPerSecond" : 17.95332136445242,
  "durationMs" : {
    "addBatch" : 259,
    "getBatch" : 0,
    "getEndOffset" : 1,
    "queryPlanning" : 47,
    "setOffsetRange" : 9,
    "triggerExecution" : 557,
    "walCommit" : 139
  },
  "stateOperators" : [ ],
  "sources" : [ {
    "description" : "KafkaV2[Subscribe[com.udacity.streams.purchases9999]]",
    "startOffset" : {
      "com.udacity.streams.purchases9999" : {
        "0" : 10
      }
    },
    "endOffset" : {
      "com.udacity.streams.purchases9999" : {
        "0" : 20
      }
    },
    "numInputRows" : 10,
    "inputRowsPerSecond" : 2.0157226365652083,
    "processedRowsPerSecond" : 17.95332136445242
  } ],
  "sink" : {
    "description" : "org.apache.spark.sql.execution.streaming.ConsoleSinkProvider@7fb44051"
  }
}

"""