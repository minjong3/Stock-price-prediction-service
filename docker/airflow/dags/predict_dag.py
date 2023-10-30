from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

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

run_my_python_script_task = BashOperator(
    task_id='predict',
    bash_command='docker start predict',
    dag=dag,
)
