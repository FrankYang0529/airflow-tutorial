import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator


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
    dag_id="parse_discord",
    description="parse discord table and insert into result table",
    default_args=default_args,
)


def check_last_content_timestamp(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    postgres_conn = postgres_hook.get_conn()
    postgres_cur = postgres_conn.cursor()
    postgres_cur.execute(
        "SELECT content_timestamp FROM result ORDER BY content_timestamp DESC"
    )
    result = postgres_cur.fetchone()
    if result is None:
        return "parse_all_content"

    context["task_instance"].xcom_push(key="timestamp", value=result[0].isoformat())
    return "parse_content_since_last_timestamp"


branching_op = BranchPythonOperator(
    task_id="branching",
    python_callable=check_last_content_timestamp,
    provide_context=True,
    dag=dag,
)


def parse_all_content(**context):
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    postgres_conn = postgres_hook.get_conn()
    postgres_cur = postgres_conn.cursor()
    postgres_cur.execute(
        "SELECT id, content, created_at FROM discord ORDER BY created_at ASC"
    )
    content_records = postgres_cur.fetchall()
    for content_record in content_records:
        print(content_record)
        postgres_cur.execute(
            "INSERT INTO result (content_id, content, content_timestamp) VALUES (%s, %s, %s)",
            (content_record[0], content_record[1], content_record[2].isoformat()),
        )
    postgres_conn.commit()
    return


parse_all_content_op = PythonOperator(
    task_id="parse_all_content",
    python_callable=parse_all_content,
    provide_context=True,
    dag=dag,
)


def parse_content_since_last_timestamp(**context):
    last_timestamp = context["task_instance"].xcom_pull(
        task_ids="branching", key="timestamp"
    )
    logging.info(f"last timestamp: {last_timestamp}")
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    postgres_conn = postgres_hook.get_conn()
    postgres_cur = postgres_conn.cursor()
    postgres_cur.execute(
        f"SELECT id, content, created_at FROM discord WHERE created_at > timestamp '{last_timestamp}' ORDER BY created_at ASC"
    )
    content_records = postgres_cur.fetchall()
    for content_record in content_records:
        postgres_cur.execute(
            "INSERT INTO result (content_id, content, content_timestamp) VALUES (%s, %s, %s)",
            (content_record[0], content_record[1], content_record[2].isoformat()),
        )
    postgres_conn.commit()
    return


parse_content_since_last_timestamp_op = PythonOperator(
    task_id="parse_content_since_last_timestamp",
    python_callable=parse_content_since_last_timestamp,
    provide_context=True,
    dag=dag,
)


branching_op >> [parse_all_content_op, parse_content_since_last_timestamp_op]
