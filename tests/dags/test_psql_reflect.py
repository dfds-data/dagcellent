"""Test SQL reflection on PostrgeSQL."""

from __future__ import annotations

import datetime

from airflow import DAG

from dagcellent.operators.sql_reflect import SQLReflectOperator

CONN_ID = "postgres_test"
DAG_ID = __file__.rstrip(".py").split("/")[-1]

with DAG(
    dag_id=DAG_ID,
    description=__doc__,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    reflect_table = SQLReflectOperator(
        table_name="ats",
        task_id="reflect_database",
        conn_id=CONN_ID,
    )

    reflect_table
