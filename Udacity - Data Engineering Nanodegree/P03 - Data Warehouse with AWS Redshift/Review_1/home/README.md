# Project: Data Warehouse
## Summary and Details :

1. We have a startup called Sparkify.
2. Sparkify wants move their processes and data onto the cloud.
3. Data resides in AWS S3 in 2 separate directories.
    - directory of JSON logs on user activity on their app.
    - directory of JSON metadata on the songs that are available on their app.
6. Sparkify wants a data engineer build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team.
 
 
## Required tasks :
1. build an ETL pipeline for a database hosted on Redshift. 
2. load data from S3 to staging tables on Redshift
3. execute SQL statements that create the analytics tables from these staging tables.
4. Test database and ETL pipeline by running queries given by the analytics team from Sparkify.
5. Verify that test results match expected results that were given by Sparkify team.
 
 
## Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals :
Building a well designed and optimized data warehouse to by used by analytics team at Sparkify is very crucial for their business. \
Sparkify wants to utilize the power of the cloud computing and build thier data warehouse in the clodu.\
They want to use the data they collect to enhance their app and having a better understanding of their users’ behaviour and needs.The data provides detailed view for\
what songs users are listening to, how much time they spend listening to a specific song,what software they're using to access the app, and which data/time.\
By utilizing the songs/artists metadata and the user logs activity, Sparkie would be able :
- Understand users' taste in music and what songs have highest play rate.
- Implementing better data quality measurements.
- getting better statistics on artists with high demand
- identify the peak time of the day for their app.
- identify what locations their app is being used which in turn could enhance their marketing strategy and targeted advertising.
- More efficient resources allocation for development team by focusing on enhancing user agent software that used most by users.
 
 
## State and justify your database schema design and ETL pipeline
### database schema :
The star schema was proposed and I believe  it's the best fit for our expected analytical database, as database consists of just one fact table and 4 dimension tables.\
Star schema will help Sparkify analytic team to write simple and fast queries to get insights about their app, and it'll give the team the ability to run fast aggregations on the data.\
I've tried to achieve 3rd form normalization for dimension tables where appropriate.
The most appropriate data type was used and primary key constraint was enforced on \
all tables to enhance data integrity and join performance.
 
### ETL pipeline :
- First, I completed ***sql_queries.py*** with appropriate sql statements, quality checks and data distribution style.
- Then, I Launched a redshift cluster and created IAM role with the appropriate access permissions.
- I've updated ***dwh.cfg*** file with required configs.
- Then, I ran ***create_tables.py*** to create the required staging tables and fact/dims tables.
- Then, I ran ***etl.py*** to stage data from S3 bucket, then transformed them into our fact/dims tables.
- Finally, I used my ***analytic_dashboard.ipynb*** to query the database and create some analytical queries.
 
### What's in my repo :
- ***sql_queries.py*** : python script contains sql statements to create staging tables and fact/dims tables.
- ***create_tables.py*** : python script to run *sql_queries.py*
- ***etl.py*** : python script, it's our actual ETL pipeline that process the move data from S3 to staging tables in Redshift database, then transformed in fact/dims table.
- ***analytic_dashboard.ipynb*** : jupyter notebook I've built that contain useful queries on Sparkify new database. 
 
### How to run the code :
1. Launch a redshift cluster and created IAM role with the appropriate access permissions
2. updated ```dwh.cfg``` file with required configs
3. from python shell run ```python create_tables.py``` to create the staging tables and fact/dims tables.
4. from python shell run ```python etl.py``` to run ETL pipeline.
 
 
## Provide example queries and results for song play analysis
Please see ***Analytic_dashboard.ipynb*** as it contains all different kinds of analytical queries on our new database.
 
