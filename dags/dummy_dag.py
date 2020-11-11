from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator


with DAG("dummy_dag", start_date=datetime(2020, 11, 11)) as dag:
    op = DummyOperator(task_id="op")
