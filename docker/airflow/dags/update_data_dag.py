from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import subprocess

default_args = {
    'owner': 'Admin',
    'depends_on_past': False,
    'retries': 10,
    'retry_delay': timedelta(minutes=3),
}

dag = DAG(
    'update_data',
    default_args=default_args,
    description='update_data',
    schedule_interval='00 06 * * 1-5',  # 월 화 수 목 일 진행
    start_date=datetime(2023, 10, 29),
    catchup=False,
    tags=['update_data'],
)

def run_update_data():
    # "python3 update_data.py" 명령을 실행
    subprocess.run(["python3", "update_data.py"])

update_data_task = PythonOperator(
    task_id='update_data',
    python_callable=run_update_data,
    dag=dag,
)

update_data_task
