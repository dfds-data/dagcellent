from __future__ import annotations

import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

DAG_ID = "postgres_operator_dag"
CONN_ID = "postgres_test"

with DAG(
    dag_id=DAG_ID,
    start_date=datetime.datetime(2020, 2, 2),
    schedule="@once",
    catchup=False,
) as dag:
    create_pet_table = SQLExecuteQueryOperator(
        task_id="create_pet_table",
        conn_id=CONN_ID,
        sql="""
            CREATE TABLE IF NOT EXISTS pet (
            pet_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            name VARCHAR NOT NULL,
            pet_type VARCHAR NOT NULL,
            birth_date DATE NOT NULL,
            OWNER VARCHAR NOT NULL);
          """,
    )

    create_pet_table
