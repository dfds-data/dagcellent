from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule
from operators.dag_onprem.external_table_arrow import CreateExternalTableArrow
from operators.dag_onprem.new_sql_s3 import BatchSqlToS3Operator

# Adding operators module to syspath
from pendulum import datetime

if TYPE_CHECKING:
    from airflow.models.taskinstance import TaskInstance

DAG_ID = "passenger_onprem-to-cloud_slow-tables_compass-load"

default_args = {
    "depends_on_past": False,
    "email_on_retry": False,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description="slow tables from onprem to cloud",
    schedule="0 1 * * *",
    start_date=datetime(2024, 8, 1),
    is_paused_upon_creation=True,
    max_active_tasks=2,
    max_active_runs=2,
    catchup=False,
    render_template_as_native_obj=True,
) as dag:
    # BUCKET
    # we always use the following s3 path:
    # <bucket name>/airflow/<table name>/<? if not partition: dump.parquet>
    #                                   /<partition name>/dump.parquet
    # s3_bucket_cnv = Variable.get(
    #    "S3_bucket_passenger", default_var="dfds-passenger-staging"
    # )
    database = "PAXDW_Prod"
    target_database = database.lower()
    schema_name = "dbo"
    target_schema_name = "src"
    aws_conn_id = "aws_dataplatform"
    sql_conn_id = "bia_mssql"
    s3_bucket = "dfds-passenger-dev"
    replace = True
    TABLES = [
        "t_D_ArrangementSubType",
        "t_D_CabinRoom",
        "t_D_CostRevenueElement",
        "t_D_Country",
        "t_D_CustomerType",
        "t_D_Gender",
        "t_D_PaxCategory",
        "t_D_RetailStore",
        "t_D_RouteLeg",
        "t_D_SalesChannel",
        "t_D_SalesOwner",
        "t_D_Segment",
        "t_D_VehicleType",
    ]

    for table_name in TABLES:
        with TaskGroup(group_id=table_name) as full_load:
            target_table_name = table_name.lower()

            load = BatchSqlToS3Operator(
                # no query provided, we are copying every table
                # query is built internally (with sqlalchemy)
                #
                database=database,
                schema_name=schema_name,
                table_name=table_name,
                task_id="load",
                queue="onprem",
                sql_conn_id=sql_conn_id,
                s3_bucket=s3_bucket,
                s3_key=f"airflow/{target_database}/{target_table_name}/dump.parquet",
                aws_conn_id="aws_dataplatform",
                file_format="parquet",
                replace=True,
                pd_kwargs={
                    "engine": "pyarrow",
                    "version": "2.6",
                    "coerce_timestamps": "us",
                },
            )

            check_table_exists = RedshiftSQLOperator(
                task_id="check_table_exists",
                trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
                redshift_conn_id="redshift_test",
                sql=f"SELECT EXISTS (SELECT * FROM SVV_EXTERNAL_TABLES where tablename = '{target_table_name}');",
                autocommit=True,
            )

            create_table_query_arrow = CreateExternalTableArrow(
                task_id="CreateExternalTableArrow",
                database=database,
                schema_name=schema_name,
                table_name=table_name,
                sql_conn_id=sql_conn_id,
                target_conn_id="redshift",
                type_map=(
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".load', key='type_map') }}"
                ),
                s3_location=(
                    f"s3://{s3_bucket}/"
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".load', key='target_file_path') }}"
                ),
                # drop if schema changes exist
                force_drop=False,
                external_schema_name=target_schema_name,
                queue="onprem",
            )

            @task.branch(
                task_id="branch_create_task",
            )
            def branch_create_func(**context: Any) -> str | None:
                """If partition query is created, run it."""
                ti: TaskInstance = context["ti"]
                group_id = ti.task_id.split(".")[0]
                xcom_value = ti.xcom_pull(task_ids=f"{group_id}.check_table_exists")
                # expected format: return_value ([False])
                table_exists = str(xcom_value).lower()
                if "false" in table_exists:
                    return f"{group_id}.execute_create_query"
                else:
                    # skip create query
                    return None

            branch_create_task = branch_create_func()

            empty_task = EmptyOperator(task_id="empty_task")

            execute_create_query = RedshiftSQLOperator(
                task_id="execute_create_query",
                redshift_conn_id="redshift_test",
                sql=(
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".CreateExternalTableArrow') }}"
                ),
                # NOTE: autocommit is necessary for 'CREATE EXTERNAL TABLE' DDL statements
                #   in Redshift/Spectrum
                autocommit=True,
            )

            (
                load
                >> check_table_exists
                >> create_table_query_arrow
                >> branch_create_task
                >> [execute_create_query, empty_task]
            )
