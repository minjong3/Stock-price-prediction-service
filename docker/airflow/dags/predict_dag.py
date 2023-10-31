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
    'predict',
    default_args=default_args,
    description='predict',
    schedule_interval='00 06 * * 1-5',  # 월 화 수 목 일 진행
    start_date=datetime(2023, 10, 29),
    catchup=False,
    tags=['predict'],
)

def run_predict():
    # "python3 predict.py" 명령을 실행
    subprocess.run(["python3", "predict.py"])

predict_task = PythonOperator(
    task_id='predict',
    python_callable=run_predict,
    dag=dag,
)

predict_task
