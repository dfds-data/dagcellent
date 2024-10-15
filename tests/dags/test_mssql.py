from __future__ import annotations

import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

DAG_ID = "mssql_operator_dag"
CONN_ID = "mssql_test"

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
        IF (EXISTS (SELECT *
             FROM INFORMATION_SCHEMA.TABLES
             WHERE TABLE_NAME = 'pet'))
        BEGIN
            CREATE TABLE pet (
            pet_id INT IDENTITY(1, 1) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            pet_type VARCHAR(255) NOT NULL,
            birth_date DATE NOT NULL,
            OWNER VARCHAR(255) NOT NULL)
        END
          """,
    )

    create_pet_table
