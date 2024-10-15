from __future__ import annotations

import datetime

from airflow import DAG
from dagcellent.operators.sql_reflect import SQLReflectOperator

CONN_ID = "mssql_test"

with DAG(
    dag_id="mssql_reflect",
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    reflect_table = SQLReflectOperator(
        task_id="reflect_database",
        conn_id=CONN_ID,
        table_name="pet",
    )

    reflect_table
