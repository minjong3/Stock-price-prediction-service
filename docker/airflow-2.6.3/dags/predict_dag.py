from airflow import DAG
from datetime import datetime
from custom_operators.predict_operator import predictOperator

default_args = {
    'owner': 'Admin',
    'depends_on_past': False,
    'retries': 10,
}

# DAG 정의
dag = DAG(
    'predict_dag', 
    default_args=default_args, 
    schedule_interval='10 06 * * 1,2,3,4,7',
    start_date=datetime(2023, 11, 1),
    )

# predictOperator 인스턴스화하고 script_path를 설정
predict_task = predictOperator(
    task_id='predict_task',
    script_path="/opt/airflow/dags/pythonfile/predict.py",
    dag=dag,  # 이 Task를 DAG에 추가
)