from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from tasks.download import download_raw_data

with DAG(
    dag_id='download_data',
    description='Download raw data from Internet',
    tags=['Rakuten'],
    schedule=None,
    default_args={
        'owner': 'airflow',
        "start_date": datetime(2025, 6, 15),
    },
    catchup=False
) as dag:
    
    task = PythonOperator(
        task_id='download_raw_data',
        python_callable=download_raw_data,
    )
    
 