import random
import string
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "pycon",
    "depends_on_past": False,
    "start_date": datetime(2020, 11, 11),
    "email": ["airflow@pycon.tw"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    "schedule_interval": "*/1 * * * *",
    # 'end_date': datetime(2020, 2, 29),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
}


dag = DAG(
    dag_id="discord",
    description="generate random string to discord table",
    default_args=default_args,
)


def generate_random_string():
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=100))


generate_data = PostgresOperator(
    task_id="generate_data",
    sql=f"INSERT INTO discord (content) VALUES ('{generate_random_string()}');",
    postgres_conn_id="postgres_default",
    autocommit=True,
    dag=dag,
)

generate_data
