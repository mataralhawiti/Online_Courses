from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from helpers.data_lake_etl import create_spark_session, process_immigration, process_temperature,\
                              process_airports, process_us_demographic, copy_to_s3, list_objs_s3

# S3 buckets
S3_BUCKET_IN = "s3a://dend-capstone-raw/"
S3_BUCKET_OUT = "s3a://dend-capstone/"

# data files
IMMIGRATION_FILE = "immigration/*.parquet"
TEMPERATURE_FILE = "GlobalLandTemperaturesByState.csv"
AIRPORTS_FILE = "airport-codes_csv.csv"
US_DEMOGRAPHIC_FILE = "us-cities-demographics.csv"


LOOKUP_FILES = ['I94addr.json', 'airlines_iata_codes.json', 'I94port.json', 'I94res.json']
FILES_MAPPING = {'I94addr.json' : 'us_states/us_states.json', 
                 'airlines_iata_codes.json' : 'airlines_iata/airlines_iata.json',
                 'I94port.json' : 'us_ports/us_ports.json',
                 'I94res.json' : 'countries/countries.json'
                }

# set dags default args
DEFAULT_ARGS = {
    'owner': 'Matar',
    'start_date': datetime.utcnow() ,
    'depends_on_past': False,
    'catchup': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# our main dag
dag = DAG('data_lake_dag',
          default_args=DEFAULT_ARGS,
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
    op_kwargs={'input_data':S3_BUCKET_IN, 'data_file':IMMIGRATION_FILE, 'output_data':S3_BUCKET_OUT},
    dag=dag
)

process_temperature = PythonOperator(
    task_id='process_temperature',
    python_callable=process_temperature,
    op_kwargs={'input_data':S3_BUCKET_IN, 'data_file':TEMPERATURE_FILE, 'output_data':S3_BUCKET_OUT},
    dag=dag
)

process_airports = PythonOperator(
    task_id='process_airports',
    python_callable=process_airports,
    op_kwargs={'input_data':S3_BUCKET_IN, 'data_file':AIRPORTS_FILE, 'output_data':S3_BUCKET_OUT},
    dag=dag
)

process_us_demographic = PythonOperator(
    task_id='process_us_demographic',
    python_callable=process_us_demographic,
    op_kwargs={'input_data':S3_BUCKET_IN, 'data_file':US_DEMOGRAPHIC_FILE, 'output_data':S3_BUCKET_OUT},
    dag=dag
)

copy_to_s3 = PythonOperator(
    task_id='copy_to_s3',
    python_callable=copy_to_s3,
    op_kwargs={'lookup_files':LOOKUP_FILES, 'files_mapping':FILES_MAPPING},
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


