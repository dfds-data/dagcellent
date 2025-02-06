from __future__ import annotations

import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from dagcellent.operators.sql_reflect import SQLReflectOperator

CONN_ID = "mssql_test"
DAG_ID = __file__.rstrip(".py").split("/")[-1]

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    reflect_table = SQLReflectOperator(
        task_id="reflect_database", conn_id=CONN_ID, table_name="kaka", database="model"
    )

    execute = SQLExecuteQueryOperator(
        task_id="execute_query",
        conn_id=CONN_ID,
        sql=reflect_table.output,  # type: ignore
        database="model",
    )

    reflect_table >> execute
