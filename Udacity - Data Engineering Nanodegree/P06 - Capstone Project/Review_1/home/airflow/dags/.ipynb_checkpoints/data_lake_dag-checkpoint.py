from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from helpers.data_lake_etl import create_spark_session, process_immigration, process_temperature,\
                              process_airports, process_us_demographic, copy_to_s3, list_objs_s3

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

# set dags default args
default_args = {
    'owner': 'Matar',
    'start_date': datetime.utcnow() ,
    'depends_on_past': False,
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# our main dag
dag = DAG('data_lake_dag',
          default_args=default_args,
          description='Load from S3, and transform data using Spark, then write data out to S3 with Airflow',
          schedule_interval='@monthly'
        )

### tasks start from here
start_operator = DummyOperator(
    task_id='Begin_execution',
    dag=dag
)

process_immigration = PythonOperator(
    task_id='process_immigration',
    python_callable=process_immigration,
    op_kwargs={'input_data':s3_bucket_in, 'data_file':immigration_file, 'output_data':s3_bucket_out},
    dag=dag
)

process_temperature = PythonOperator(
    task_id='process_temperature',
    python_callable=process_temperature,
    op_kwargs={'input_data':s3_bucket_in, 'data_file':temperature_file, 'output_data':s3_bucket_out},
    dag=dag
)

process_airports = PythonOperator(
    task_id='process_airports',
    python_callable=process_airports,
    op_kwargs={'input_data':s3_bucket_in, 'data_file':airports_file, 'output_data':s3_bucket_out},
    dag=dag
)

process_us_demographic = PythonOperator(
    task_id='process_us_demographic',
    python_callable=process_us_demographic,
    op_kwargs={'input_data':s3_bucket_in, 'data_file':us_demographic_file, 'output_data':s3_bucket_out},
    dag=dag
)

copy_to_s3 = PythonOperator(
    task_id='copy_to_s3',
    python_callable=copy_to_s3,
    op_kwargs={'lookup_files':lookup_files, 'files_mapping':files_mapping},
    dag=dag
)

list_objs_s3 = PythonOperator(
    task_id='list_objs_s3',
    python_callable=list_objs_s3,
    dag=dag
)

end_operator = DummyOperator(
    task_id='Stop_execution',
    dag=dag
)


# set up tasks dependency
start_operator >> process_immigration

process_immigration >> process_temperature
process_immigration >> process_airports
process_immigration >> process_us_demographic
process_immigration >> copy_to_s3

process_immigration >> list_objs_s3
process_temperature >> list_objs_s3
process_airports >> list_objs_s3
process_us_demographic >> list_objs_s3
copy_to_s3 >> list_objs_s3

list_objs_s3 >> end_operator


