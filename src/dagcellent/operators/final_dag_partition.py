"""DAG that implements partitioning.

~/work/airflow_k8s_dag/db_transfer/dags/emissions_analytics/dim_tables_fast_full_load.py

```python
    sql_t_d_bookingcategory = SqlToS3Operator(
        task_id="t_d_bookingcategory_to_s3_task",
        query=f"USE {log_dm_db};{sql_t_d_bookingcategory}",
        s3_key="airflow/emissions/dim/t_d_bookingcategory/run_date={{ data_interval_end | ds }}/{{ data_interval_end | ds }}.parquet",
        **shared_task_config,
    )
```
example PR: https://dev.azure.com/dfds/The%20Compass/_git/k8s-airflow-dags/pullrequest/90497?_a=files


```python
    # Final part of both full and incremental load branches
    daily_load_to_s3_task = BatchSqlToS3Operator(
        task_id=f"daily_load_to_s3_{query_info.get('table')}",
        query=(
            f"{query_info.get('query')}"
            " WHERE apb.ProcessDate = '{{ data_interval_end | ds }}'"
            " LEFT JOIN SSISMaster.dbo.AuditProcessBatch AS apb"
            "   ON apb.ProcessBatchKey = rvc.ProcessBatchKey"
        ),
        s3_key=S3_PREFIX + "run_date={{ data_interval_end | ds }}/chunk.parquet",
        use_pyarrow_for_dtype=True,
        trigger_rule=TriggerRule.NONE_FAILED,
        pd_kwargs={
            "engine": "pyarrow",
            "version": "2.6",
            "coerce_timestamps": "us",
        },
    )

```

The generated DDL will not going to use table name short-hands.

```sql
SELECT [ReservationCode]
      ,[ReservationVersion]
      ,[DepartureKey]
      ,[CheckInStatusKey]
      ,[GenderKey]
      ,[PaxCategoryKey]
      ,[PaxCountryKey]
      ,[BirthDate]
      ,[PaxCount]
      ,rvp.[ProcessBatchKey]
  FROM [PAXDW_Prod].[dbo].[t_F_ReservationVersionPax]
  LEFT JOIN SSISMaster.dbo.AuditProcessBatch
      ON SSISMaster.dbo.AuditProcessBatch.ProcessBatchKey = [PAXDW_Prod].[dbo].[t_F_ReservationVersionPax].ProcessBatchKey;
```
so it takes the form like this:
```sql
SELECT ProductID, Purchasing.Vendor.BusinessEntityID, Name
FROM Purchasing.ProductVendor INNER JOIN Purchasing.Vendor
    ON (Purchasing.ProductVendor.BusinessEntityID = Purchasing.Vendor.BusinessEntityID)
WHERE StandardPrice > $10
  AND Name LIKE N'F%';
```
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from airflow import DAG
from airflow.decorators import task
from airflow.models.param import Param
from airflow.operators.empty import EmptyOperator
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule
from operators.dag_onprem.external_table_arrow import CreateExternalTableArrow
from operators.dag_onprem.new_sql_s3 import BatchSqlToS3Operator
from pendulum import datetime, duration

if TYPE_CHECKING:
    from airflow.models.dagrun import DagRun
    from airflow.models.taskinstance import TaskInstance

_LOGGER = logging.getLogger("airflow")

DAG_ID = "passenger_onprem-to-cloud_fast-tables_compass-load"

default_args = {
    "depends_on_past": False,
    "email_on_retry": False,
    "retry_delay": duration(minutes=2),
}

with DAG(
    dag_id=DAG_ID,
    default_args=default_args,
    description="DAG for daily load of all tables in PAXDW_Prod",
    schedule="0 1 * * *",
    start_date=datetime(2024, 8, 1),
    is_paused_upon_creation=True,
    max_active_tasks=5,
    max_active_runs=1,
    catchup=False,
    params={
        "full_refresh": Param(
            False,
            type="boolean",
            title="Full Refresh",
            description="True to load historcial data into a default 1900-01-01 partition.",
        ),
    },
    render_template_as_native_obj=True,
) as dag:
    database = "PAXDW_Prod"
    target_database = database.lower()
    schema_name = "dbo"
    target_schema_name = "src"
    aws_conn_id = "aws_dataplatform"
    sql_conn_id = "bia_mssql"
    s3_bucket = "dfds-passenger-dev"
    replace = True
    # TASKS
    TABLES = [
        "t_D_Departure",
        "t_F_Reservation",
        "t_F_ReservationPax",
        "t_F_ReservationVersion",
        "t_F_ReservationVersionArrangement",
        "t_F_ReservationVersionCabin",
        "t_F_ReservationVersionCostRevenue",
        "t_F_ReservationVersionPax",
        "t_F_ReservationVersionVehicle",
        "t_F_RetailArticleSales",
    ]
    for table_name in TABLES:
        with TaskGroup(group_id=table_name) as full_load:
            target_table_name = table_name.lower()

            @task(task_id="branch_load_type_task")
            def branch_load_type_func(
                database: str,
                schema_name: str,
                table_name: str,
                target_database: str,
                target_table_name: str,
                **context: Any,
            ) -> dict[str, str]:
                """Determine if historical or daily load."""
                ti: TaskInstance = context["ti"]
                dag_run: DagRun = ti.dag_run
                data_interval_end = dag_run.data_interval_end.strftime("%Y-%m-%d")
                # scheduled trigger
                if not dag_run.external_trigger:
                    _LOGGER.debug("Triggered by schedule")

                try:
                    is_full_refresh = context["params"]["full_refresh"]
                except KeyError as e:
                    _LOGGER.error("No full_refresh parameter found")
                    raise e

                if is_full_refresh is True:
                    # return _historical_load
                    return {
                        "s3_key": (
                            f"airflow/{target_database}/{target_table_name}/"
                            "run_date=1900-01-01"
                        ),
                        # NOTE: where clause is only allowed for filtering
                        "where_clause": f"WHERE [SSISMaster].dbo.AuditProcessBatch.ProcessBatchKey IS NULL OR [SSISMaster].dbo.AuditProcessBatch.ProcessDate < '{data_interval_end}'",
                        # NOTE: join is only allowed for filtering
                        "join_clause": f"LEFT JOIN [SSISMaster].dbo.AuditProcessBatch ON [SSISMaster].dbo.AuditProcessBatch.ProcessBatchKey = [{database}].{schema_name}.{table_name}.ProcessBatchKey",
                    }
                # return _daily_load
                else:
                    return {
                        "s3_key": (
                            f"airflow/{target_database}/{target_table_name}/"
                            f"run_date={data_interval_end}"
                        ),
                        # NOTE: where clause is only allowed for filtering
                        "where_clause": f"WHERE [SSISMaster].dbo.AuditProcessBatch.ProcessDate = '{data_interval_end}'",
                        # NOTE: join is only allowed for filtering
                        "join_clause": f"LEFT JOIN [SSISMaster].dbo.AuditProcessBatch ON [SSISMaster].dbo.AuditProcessBatch.ProcessBatchKey = [{database}].{schema_name}.{table_name}.ProcessBatchKey",
                    }

            branch_load_type_task = branch_load_type_func(
                database=database,
                schema_name=schema_name,
                table_name=table_name,
                target_database=target_database,
                target_table_name=target_table_name,
            )

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
                s3_key=(
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".branch_load_type_task', key='s3_key') }}"
                ),
                aws_conn_id="aws_dataplatform",
                file_format="parquet",
                replace=True,
                pd_kwargs={
                    "engine": "pyarrow",
                    "version": "2.6",
                    "coerce_timestamps": "us",
                },
                # NOTE: where clause is only allowed for filtering
                where_clause=(
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".branch_load_type_task', key='where_clause') }}"
                ),
                # NOTE: join is only allowed for filtering
                join_clause=(
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".branch_load_type_task', key='join_clause') }}"
                ),
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
                partitioned=(
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".load', key='partitioned') }}"
                ),
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
                    return f"{group_id}.empty_task"

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

            @task.branch(
                task_id="branch_add_partition",
                trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
            )
            def branch_partition_func(**context: Any) -> str | None:
                """If partition query is created, run it."""
                ti: TaskInstance = context["ti"]
                group_id = ti.task_id.split(".")[0]
                xcom_value = ti.xcom_pull(
                    task_ids=f"{group_id}.CreateExternalTableArrow",
                    key="partition_query",
                )
                if xcom_value:
                    return f"{group_id}.add_partition_query"
                else:
                    # skip all downstream tasks
                    return None

            branch_add_partition = branch_partition_func()

            add_partition_query = RedshiftSQLOperator(
                task_id="add_partition_query",
                redshift_conn_id="redshift_test",
                sql=(
                    "{{ ti.xcom_pull(task_ids='"
                    f"{table_name}"
                    ".CreateExternalTableArrow', key='partition_query') }}"
                ),
                autocommit=True,
            )
            # Task dependencies
            # NOTE: Indentation has to be under the TaskGroup
            (
                branch_load_type_task
                >> load
                >> check_table_exists
                >> create_table_query_arrow
                >> branch_create_task
                >> [execute_create_query, empty_task]
                >> branch_add_partition
                >> [add_partition_query]
            )

        full_load
