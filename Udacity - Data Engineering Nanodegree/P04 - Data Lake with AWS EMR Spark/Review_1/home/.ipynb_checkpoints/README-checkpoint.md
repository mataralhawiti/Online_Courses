# Project: Data Lake
## Summary and Details :

1. We have a startup called Sparkify.
2. Sparkify wants move their warehouse to a data lake.
3. Data resides in AWS S3 in 2 separate directories.
    - directory of JSON logs on user activity on their app.
    - directory of JSON metadata on the songs that are available on their app.
4. Sparkify wants a data engineer to build an ETL pipeline that extracts their data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables. for their analytics team.
 
 
## Required tasks :
1. Build an ETL pipeline for a data lake hosted on S3 using Spark.
2. Extract data from S3, processes them using Spark and then load the data back into S3 as a set of dimensional tables.
3. Deploy Spark process on a cluster using AWS to run python spark application
 
 
## Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals :
Building a well designed and orgainzed data lake to by used by analytics team at Sparkify is very crucial for their business. \
Sparkify wants to utilize the power of the cloud computing and move thier warehouse to data lake in the cloud, AWS.
They want to use the data they collect to enhance their app and having a better understanding of their users’ behaviour and needs. \
The data provides detailed view for what songs users are listening to, how much time they spend listening to a specific song,what software they're using to access the app, and which data/time.\
By utilizing the songs/artists metadata and the user logs activity, Sparkie would be able :
- Understand users' taste in music and what songs have highest play rate.
- Implementing better data quality measurements.
- getting better statistics on artists with high demand
- identify the peak time of the day for their app.
- identify what locations their app is being used which in turn could enhance their marketing strategy and targeted advertising.
- More efficient resources allocation for development team by focusing on enhancing user agent software that used most by users.
 
 
## State and justify your database schema design and ETL pipeline
### Data lake design :
we'll utilize EMR spark cluster to process our songs and logs data from AWS S3 buckets.
After processing, we'll write our dimensional tables to another AWS S3 buckets.
Related table files will be written to a separate directory.
Finally, We'll efficiently store our files using columnar storage format Parquet.
 
### ETL pipeline :
- I've updated ***dl.cfg*** file with required configs.
- First, I completed ***etl.py*** with appropriate python code.
- Then, I Launched a EMR spark cluster.
- Then, I ran ***etl.py*** to test my code with the provided sample data.
- Then, I created AWS S3 bucket to be used for our output files.
- Finally, I ran ***etl.py*** to process songs/logs data from AWS S3 input bucket, and store the output in the created S3 bucket.

 
### What's in my repo :
- ***etl.py*** : python script, it's our actual ETL pipeline that extracts data from S3, processes them using Spark, and loads the data back into S3 as a set of dimensional tables
- ***data and playground*** : folders for data and my testing files.
 
### How to run the code :
1. Launch a EMR spark cluster
2. updated ```dl.cfg``` file with required configs
3. Create AWS S3 bucket and update ```python etl.py``` with the correct output name variable.
4. from python shell run ```python etl.py``` to run ETL pipeline.
