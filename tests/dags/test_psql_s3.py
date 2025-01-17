"""Test SQL reflection on PostrgeSQL."""
from __future__ import annotations

import datetime

from airflow import DAG

from dagcellent.operators import SqlToS3Operator
from dagcellent.operators.sql_reflect import SQLReflectOperator

DAG_ID = __file__.rstrip(".py").split("/")[-1]
CONN_ID = "postgres_test"
AWS_CONN_ID = "dummy"
S3_BUCKET = "dummy"

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

    sql_to_s3 = SqlToS3Operator(
        task_id="to_s3",
        query=reflect_table.output,
        database="doesnt matter",
        sql_conn_id=CONN_ID,
        s3_bucket=S3_BUCKET,
        s3_key="airflow/wms_test/lea_inbounddocument/full_load.parquet",
        aws_conn_id=AWS_CONN_ID,
        file_format="parquet",
        replace=True,
        pd_kwargs={
            "engine": "pyarrow",
            "version": "2.6",
            "coerce_timestamps": "us",
        },
    )

    reflect_table >> sql_to_s3  # pyright: ignore[reportUnusedExpression]
