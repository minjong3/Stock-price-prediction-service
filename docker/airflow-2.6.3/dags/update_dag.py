from airflow import DAG
from datetime import datetime
from custom_operators.update_operator import UpdateDataOperator

default_args = {
    'owner': 'Admin',
    'depends_on_past': False,
    'retries': 10,
}

# DAG 정의
dag = DAG(
    'data_update_dag', 
    default_args=default_args, 
    schedule_interval='00 06 * * 1-5',
    start_date=datetime(2023, 11, 1),
    )

# UpdateDataOperator를 인스턴스화하고 script_path를 설정
data_update_task = UpdateDataOperator(
    task_id='data_update_task',
    script_path="/opt/airflow/dags/pythonfile/update_data.py",
    dag=dag,  # 이 Task를 DAG에 추가
)