from __future__ import annotations

from typing import Any

from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from dagcellent.data_utils.sql_reflection import (
    reflect_meta_data,
    reflect_select_query,
)


class SQLReflectOperator(SQLExecuteQueryOperator):
    """Operator to perform SQLAlchemy like database reflection.

    The target_table is returned as a `SELECT` statement DDL.

    Example
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
        table_name: str | None,
        **kwargs: Any,
    ) -> None:
        self.table_name = table_name
        super().__init__(sql="", **kwargs)  # type: ignore

    def execute(self, context: Any):
        hook = self.get_db_hook()
        self.log.debug("Target connection: %s", hook.get_conn())
        engine = hook.get_sqlalchemy_engine()  # type: ignore
        # inject database name if not defined in connection URI
        # This works, but cannot cross query/reflect properly

        meta_data = reflect_meta_data(engine)  # type: ignore
        if meta_data.tables is None:  # type: ignore[reportUnnecessaryCondition]
            raise ValueError("No metadata found for the database.")

        self.log.debug("::group::🦆")
        _tables = meta_data.tables.keys()
        self.log.debug("Tables: %s", _tables)
        self.log.debug("::endgroup::")
        try:
            target_table = meta_data.tables[self.table_name]
        except KeyError:
            self.log.debug(
                "Table %s not found.\nTables found: %s", self.table_name, _tables
            )
            raise ValueError(f"Table {self.table_name} not found in the database.")

        # TODO: FIX dbname and schema name target_table.schema = f"[{self.database}].[dbo]"
        select_ddl = reflect_select_query(target_table, engine)  # type: ignore
        return select_ddl
