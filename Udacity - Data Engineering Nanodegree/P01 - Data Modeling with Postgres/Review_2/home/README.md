# Project: Data Modeling with Postgres
## Summary and Details :
1. We have a startup called Sparkify.
1. Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. 
3. The analytics team want to understand what songs users are listening to.
4. Sparkify doesn't have an easy way to query their data.
5. Data resides 2 separate directories.
    - directory of JSON logs on user activity on their app.
    - directory of JSON metadata on the songs that are available on their app.
6. Sparkify wants a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis.
 
## Required tasks :
1. Create a database schema and ETL pipeline for this analysis. 
2. Test database and ETL pipeline by running queries given by the analytics team from Sparkify.
3. Verify that test results match expected results that were given by Sparkify team.
 
 
## Discuss the purpose of this database in the context of the startup, Sparkify, and their analytical goals :
Building a well designed and optimized database to by used by analytics team at Sparkify is very crucial for their business. \
Sparkify wants to utilize the data they collect to enhance their app and having a better understanding of their users’ behaviour and needs.The data provides detailed view for\
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
- First, I completed ***sql_queries.py*** with appropriate sql statements.
- Then, I ran ***create_tables.py*** to create the database and the required tables.
- I've utilized the provided ***etl.ipynb*** notebook to build inialie ETL pipeline on small set of the data.
- I utilized ***Pandas*** module for python to make it easier to work with data.
- I took advantage ***test.ipynb*** to test my ***etl.ipynb*** code.
- After being confident I've achieved the correct code assignment in the notebook on a small sample of the data I moved to ***etl.py***
- I used what I've learned from working on notebook to build my ETL pipeline.
- I tried to use the most efficient way to manipulate Pandas dataframe, write pythonic code, handle the errors and expected scenarios in the code.
 
### What's in my repo :
- ***data*** : a directory contains songs data directory and logs data directory as well.
- ***sql_queries.py*** : python script contains sql statements to create the database and the required tables.
- ***create_tables.py*** : python script to run *sql_queries.py*
- ***etl.ipynb*** : jupyter notebook I used to build my initial ETL pipeline on small dataset, and it makes it easier for interactive development.
- ***test.ipynb*** : jupyter notebook to test our code.
- ***etl.py*** : python script, it's our actual ETL pipeline that process the entire data.
- ***analytic_dashboard.ipynb*** : jupyter notebook I've built that contain useful queries on Sparkify new database. 
- ***Backups*** : it's a directory I used for backup, please ignore it.
 
### How to run the code :
1. from python shell run ```python create_tables.py``` to create the database and the tables.
2. Start *etl.ipynb* jupyter notebook and follow the instructions to build ETL pipeline step by step.
3. Start *test.ipynb* jupyter notebook and run provided tests to test your code.
4. Once you completed *etl.py*, from python shell run ```python etl.py``` to run ETL pipeline on the enitre data.
5. use *test.ipynb* to test again.
 
 
## Provide example queries and results for song play analysis
Please see ***analytic_dashboard.ipynb*** as it contains all different kinds of analytical queries on our new database.
 
