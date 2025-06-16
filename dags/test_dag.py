from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.hooks.base import BaseHook
import boto3

def list_minio_buckets(**context):
    conn = BaseHook.get_connection('minio_default')  # conn_id

    s3 = boto3.client(
        's3',
        endpoint_url=f"http://{conn.host}:{conn.port}",
        aws_access_key_id=conn.login,
        aws_secret_access_key=conn.password,
    )

    buckets = s3.list_buckets()
    print("Buckets:", [b['Name'] for b in buckets['Buckets']])

with DAG(
    dag_id="test_minio_connection",
    start_date=datetime(2023, 1, 1),
    schedule=None, 
    catchup=False,
    tags=["rakuten", "minio"],
) as dag:

    test_connection = PythonOperator(
        task_id="list_buckets",
        python_callable=list_minio_buckets,
    )