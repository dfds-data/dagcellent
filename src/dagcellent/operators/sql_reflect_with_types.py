from __future__ import annotations

from typing import TYPE_CHECKING, Any

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from sqlalchemy import ReflectedColumn, cast, inspect, select

from dagcellent.data_utils.sql_reflection import (
    reflect_meta_data,
    safe_add_database_to_connection,
)

if TYPE_CHECKING:
    from sqlalchemy.engine.interfaces import ReflectedColumn


class SQLReflectOperator(SQLExecuteQueryOperator):
    """Operator to perform SQLAlchemy like database reflection.

    The target_table is returned as a `SELECT` statement DDL.

    Example:
        The example below illustrates a PostrgeSQL database and the
        returned SELECT query.

        ```sql
        CREATE TABLE IF NOT EXISTS ats
        (
            departure_id varchar(40) COLLATE pg_catalog."default" NOT NULL,
            route_leg_code varchar(40) COLLATE pg_catalog."default" NOT NULL,
            planned_departure_date_time timestamp without time zone NOT NULL,
            ferry_name varchar(40) COLLATE pg_catalog."default" NOT NULL,
            cnv_outlet varchar(40) COLLATE pg_catalog."default" NOT NULL,
            store_name varchar(40) COLLATE pg_catalog."default" NOT NULL,
            store_item varchar(200) COLLATE pg_catalog."default" NOT NULL,
            predicted_sales double precision NOT NULL,
            good boolean DEFAULT false,
            CONSTRAINT ats_pkey PRIMARY KEY (departure_id, route_leg_code, ferry_name, cnv_outlet, store_name, store_item)
        );
        ```

        ```python
        reflect_table = SQLReflectOperator(
            table_name="ats",
            task_id="reflect_database",
            conn_id=CONN_ID,
        )
        ```

        ```sql
        SELECT
            ats.departure_id,
            ats.route_leg_code,
            ats.planned_departure_date_time,
            ats.ferry_name,
            ats.cnv_outlet,
            ats.store_name,
            ats.store_item,
            ats.predicted_sales,
            ats.good
        FROM ats
        ```
    """

    def __init__(
        self,
        *,
        table_name: str,
        database: str | None = None,
        schema: str | None = None,
        **kwargs: Any,
    ) -> None:
        """Init.

        Args:
            table: target table name
            kwargs: additional arguments to pass to SQLExecuteQueryOperator
        """
        # TODO: deprecate this, for now inheritance needs debugging
        self.database_name = database
        kwargs["database"] = database
        self.table_name = table_name
        self.schema = schema
        super().__init__(sql="", **kwargs)  # type: ignore

    def execute(self, context: Any):
        hook = self.get_db_hook()
        engine = hook.get_sqlalchemy_engine()  # type: ignore
        self.log.debug("%s", f"{self.database_name=}")
        if self.database_name:
            # inject database name if not defined in connection URI
            self.log.debug("Target connection: %s", f"{engine.url.database=}")
            engine = safe_add_database_to_connection(engine, self.database_name)
        self.log.debug("Target connection: %s", engine.url)

        table = reflect_meta_data(engine, schema=self.schema, table=self.table_name)
        if table is None:  # type: ignore[reportUnnecessaryCondition]
            raise ValueError(f"Table {self.table_name} not found in the database.")

        self.log.debug("::group::🦆")
        self.log.debug("Table: %s", table.__dict__)
        self.log.debug("::endgroup::")

        reflected_columns: ReflectedColumn = inspect(engine).get_columns(
            self.table_name
        )
        select_ddl = select(
            *[cast(col["name"], col["type"]) for col in reflected_columns]
        )

        return select_ddl
