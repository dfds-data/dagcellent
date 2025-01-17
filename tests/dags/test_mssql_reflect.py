"""Test DAG to show the usage of SQL reflection
and executing the returned query.
"""
from __future__ import annotations

import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from dagcellent.operators.sql_reflect import SQLReflectOperator

CONN_ID = "mssql_test"
DAG_ID = __file__.rstrip(".py").split("/")[-1]

with DAG(
    dag_id=DAG_ID,
    description=__doc__,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    reflect_table = SQLReflectOperator(
        table_name="test",
        task_id="reflect_database",
        conn_id=CONN_ID,
    )

    create_pet_table = SQLExecuteQueryOperator(
        task_id="create_pet_table",
        conn_id=CONN_ID,
        sql=reflect_table.output,
    )

    reflect_table >> create_pet_table
