from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

default_args = {
    'owner': 'Admin',
    'depends_on_past': False,
    'retries': 10,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'predict',
    default_args=default_args,
    description='predict',
    schedule_interval='30 06 * * 1,2,3,4,7',  # 월 화 수 목 일 진행
    start_date=datetime(2023, 10, 29),
    catchup=False,
    tags=['predict'],
)

predict_task = DockerOperator(
    task_id='predict',
    image='predict deeplearning',
    auto_remove=True,
    dag=dag,
)
