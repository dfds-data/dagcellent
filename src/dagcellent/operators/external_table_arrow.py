from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from airflow.models.baseoperator import BaseOperator

from dagcellent.data_utils.sql_reflection import (
    Query,
    create_external_table_redshift_arrow,
)


class CreateExternalTableArrow(BaseOperator):
    """Create an external table in target database."""

    ui_color = "#6feeb7"
    ui_fgcolor = "#351c75"
    custom_operator_name = "Howdy🧀 "

    template_fields: Sequence[str] = (
        "target_conn_id",
        "sql_conn_id",
        "table_name",
        "s3_location",
        "type_map",
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
        type_map: dict[str, str],
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
        self.type_map = type_map
        self.s3_location = s3_location
        self.external_schema_name = external_schema_name
        self.partitioned = partitioned

    def execute(self, context: Any) -> Query:
        """Execute the operator."""
        # TODO: check if the table exists - NOT IMPLEMENTED

        self.log.info("%s", f"{type(self.type_map)} - {self.type_map}")
        self.query, partition_query = create_external_table_redshift_arrow(
            self.type_map,
            self.table_name,
            self.s3_location,
            schema_name=self.external_schema_name,
            partitioned=self.partitioned,
        )

        self.log.info("::group::Query")
        self.log.info(self.query)
        self.log.info("::endgroup::")

        self.xcom_push(context, key="query", value=self.query)
        self.xcom_push(context, key="partition_query", value=partition_query)
        message = "🍇"
        self.log.info(message)
        #  target_engine = self._get_hook(self.target_conn_id).get_sqlalchemy_engine()
        #  result = engine.execute(text(self.query))
        #  # names = [row[0] for row in result]
        #  self.log.info(f"Result: {result}")
        self.xcom_push(context, key="query", value=self.query)
        return self.query
