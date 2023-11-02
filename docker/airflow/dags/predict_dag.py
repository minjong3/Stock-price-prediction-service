from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

default_args = {
    'owner': 'Admin',
    'depends_on_past': False,
    'retries': 10,
    'retry_delay': timedelta(minutes=3),
}

dag = DAG(
    'predict',
    default_args=default_args,
    description='predict',
    schedule_interval='00 06 * * 1-5',  # 월 화 수 목 일 진행
    start_date=datetime(2023, 10, 29),
    catchup=False,
    tags=['predict'],
)

predict_task = BashOperator(
    task_id='predict',
    bash_command='python3 predict.py',
    dag=dag,
)

predict_task
