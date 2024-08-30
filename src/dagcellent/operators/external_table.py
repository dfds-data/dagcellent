from __future__ import annotations

from collections.abc import Sequence
from pprint import pformat
from typing import Any

from airflow.exceptions import AirflowException
from airflow.hooks.base import BaseHook
from airflow.models.baseoperator import BaseOperator
from airflow.providers.common.sql.hooks.sql import DbApiHook
from operators.dag_onprem.sql_utils.reflection import (
    Query,
    create_external_table_redshift,
    drop_unsupported_dtypes,
    reflect_meta_data,
    strip_table_constraints,
)
from sqlalchemy import create_engine


class CreateExternalTable(BaseOperator):
    """Create an external table in target database."""

    ui_color = "#6feeb7"
    ui_fgcolor = "#351c75"
    custom_operator_name = "Howdy🧀 "

    template_fields: Sequence[str] = (
        "target_conn_id",
        "sql_conn_id",
        "table_name",
        "s3_location",
        "partitioned",
    )

    def __init__(
        self,
        table_name: str,
        sql_conn_id: str,
        database: str,
        schema_name: str,
        target_conn_id: str,
        s3_location: str,
        partitioned: bool = False,
        force_drop: bool = False,
        external_schema_name: str = "src",
        **kwargs: Any,
    ) -> None:
        """Create an external table in target database.

        Args:
            table_name (str): The name of the table to create.
            sql_conn_id (str): The source connection id.
            target_conn_id (str): The target connection id.
            s3_location (str): The S3 location of the data.
            force_drop (bool, optional): If True, drop the table first. Defaults to False.
            external_schema_name (str, optional): The schema name. Defaults to "src".
            partitioned (bool, optional): Partition by `run_date`. Defaults to False.

        Raises:
            AirflowException: If the table does not exist in the source database

        Returns:
            None

        Example:
            ```python
            create_external_table = CreateExternalTable(
                task_id="create_external_table",
                table_name="my_table",
                sql_conn_id="my_conn",
                target_conn_id="my_target_conn",
                s3_location="s3://my-bucket/my-folder/",
                force_drop=True,
            )
            ```
        """
        super().__init__(**kwargs)
        self.table_name = table_name
        self.database = database
        self.schema_name = schema_name
        self.force_drop = force_drop
        self.sql_conn_id = sql_conn_id
        self.target_conn_id = target_conn_id
        self.s3_location = s3_location
        self.external_schema_name = external_schema_name
        self.partitioned = partitioned

    def _get_hook(self) -> DbApiHook:
        """Override base class method to get the hook."""
        self.log.debug("Get connection for %s", self.sql_conn_id)
        conn = BaseHook.get_connection(self.sql_conn_id)
        hook = conn.get_hook()
        if not callable(getattr(hook, "get_pandas_df", None)):
            raise AirflowException(
                "This hook is not supported. The hook class must have get_pandas_df method."
            )
        return hook

    def execute(self, context: Any) -> Query:
        """Execute the operator."""
        # TODO: check if the table exists - NOT IMPLEMENTED
        sql_hook = self._get_hook()
        engine = sql_hook.get_sqlalchemy_engine()
        engine_with_db = create_engine(str(engine.url) + f"/{self.database}")
        print(str(engine_with_db.url).split("@")[1])
        meta_data = reflect_meta_data(engine_with_db)
        if meta_data.tables is None:
            raise AirflowException(f"Tables not found in {self.sql_conn_id}")
        try:
            target_table = meta_data.tables[self.table_name]
        except KeyError as e:
            self.log.error(f"🤬 Table {self.table_name} not found.")
            self.log.error(pformat(str(meta_data.tables.keys()), indent=2))
            raise AirflowException(
                f"Table {self.table_name} not found in {self.sql_conn_id}"
            ) from e
        target_table = drop_unsupported_dtypes(target_table)
        target_table = strip_table_constraints(target_table)
        self.query = create_external_table_redshift(
            target_table,
            self.s3_location,
            schema_name=self.external_schema_name,
            partitioned=self.partitioned,
        )

        self.log.info("::group::Query")
        self.log.info(self.query)
        self.log.info("::endgroup::")

        message = "🍇"
        self.log.info(message)
        #  target_engine = self._get_hook(self.target_conn_id).get_sqlalchemy_engine()
        #  result = engine.execute(text(self.query))
        #  # names = [row[0] for row in result]
        #  self.log.info(f"Result: {result}")
        self.xcom_push(context, key="query", value=self.query)
        return self.query
