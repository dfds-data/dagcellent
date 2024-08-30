from __future__ import annotations

import random
import string
from collections.abc import Iterable, Sequence
from contextlib import closing
from typing import TYPE_CHECKING, Any, TypedDict

import pandas as pd
import pandas.io.sql as psql
from airflow.providers.amazon.aws.transfers.sql_to_s3 import (
    FILE_OPTIONS_MAP,
    NamedTemporaryFile,
    S3Hook,
    SqlToS3Operator,
)

if TYPE_CHECKING:
    from airflow.providers.amazon.aws.transfers.sql_to_s3 import FileOptions
    from airflow.utils.context import Context

import logging

from operators.dag_onprem.sql_utils.reflection import (
    Query,
    pyarrow2redshift,
    reflect_meta_data,
    reflect_select_query,
)
from pyarrow import parquet as pq
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.DEBUG)


class StoragePaths(TypedDict):
    """Cloud blob storage path and full file name."""

    path: str
    file: str


class BatchSqlToS3Operator(SqlToS3Operator):
    """Inheriting from SqlToS3Operator (v2.5.1) adding internal batching mechanism.

    Avoids running out of memory error by setting chunksize for number of rows you can move in one batch.

    Previously empty files would be written to S3 which will break the external
    tables in Redshift. Checking for empty files was added as well.

    Partitioning
    If the data is partitioned, `run_date=` partitions will be used.

    Until we have observability, we will not optimize/move away from the
    built-in provider (and pandas).

    kwargs:
        aws_conn_id: reference to a specific S3 connection
        sql_conn_id: reference to a specific database.

    # Example:

    Output query:
    ```sql
    sql_t_d_engineSource = ""
    SELECT [EngineSourceKey]
          ,[EngineSourceCode]
          ,[EngineSourceName]
      FROM [dbo].[t_D_EngineSource]
    ""
    ```
    """

    template_fields: Sequence[str] = (
        "database",
        "schema_name",
        "s3_bucket",
        "s3_key",
        "query",
        "sql_conn_id",
        "table_name",
        "where_clause",
        "join_clause",
    )

    template_ext: Sequence[str] = (".sql",)
    template_fields_renderers = {
        "where_clause": "sql",
        "join_clause": "sql",
        "query": "sql",
        "pd_kwargs": "json",
    }

    DEFAULT_PARTITION = "run_date=1900-01-01"

    def __init__(
        self,
        database: str,
        schema_name: str,
        table_name: str,
        chunksize: int = 10**6,
        format_needed: bool = True,
        where_clause: str | None = None,
        join_clause: str | None = None,
        **kwargs: Any,
    ) -> None:  # type: ignore
        """Override constructor with extra chunksize argument."""
        if kwargs.get("query", None):
            self.log.error("Query will be overwritten.")
        kwargs["query"] = "thez nutz"

        super().__init__(**kwargs)
        self.log.info(f"Query: {kwargs['query']}")
        self.chunksize = chunksize
        self.format_needed = format_needed
        self.database = database
        self.schema_name = schema_name
        self.table_name = table_name
        self.where_clause = where_clause
        self.join_clause = join_clause
        self.log.setLevel("NOTSET")

    def _create_select_query(self) -> Query:
        """Reflects the table from the database."""
        sql_hook = self._get_hook()
        engine = sql_hook.get_sqlalchemy_engine()
        # inject database name if not defined in connection URI
        # This works, but cannot cross query/reflect properly
        engine_with_db = create_engine(str(engine.url) + f"/{self.database}")

        meta_data = reflect_meta_data(engine_with_db)  # type: ignore
        if meta_data.tables is None:
            raise ValueError("No metadata found for the database.")
        try:
            target_table = meta_data.tables[self.table_name]
        except KeyError:
            print("Tables found: %s", meta_data.tables.keys())
            self.log.debug("Tables found: %s", meta_data.tables.keys())
            raise ValueError(f"Table {self.table_name} not found in the database.")
        target_table.schema = f"[{self.database}].[{self.schema_name}]"
        select_ddl = reflect_select_query(target_table, engine)  # type: ignore
        if self.join_clause:
            select_ddl = f"{select_ddl}{self.join_clause} "
        if self.where_clause:
            select_ddl = f"{select_ddl} {self.where_clause}"
        return select_ddl

    def get_pandas_data(self, sql: str) -> Iterable[pd.DataFrame]:
        """
        Rewrite of the get_pandas_df method on DbApiHook to adapt to our use case.

        Passes the chunksize to underlying pandas method for batching.

        :param sql: the sql query to run
        :type sql: str
        """
        sql_hook = self._get_hook()

        with closing(sql_hook.get_conn()) as conn:
            yield from psql.read_sql(
                sql, con=conn, params=self.params, chunksize=self.chunksize
            )

    def cleanup_s3_folder(self, s3_hook: S3Hook, path: str) -> bool:
        """
        Delete the objects in the s3 folder.

        :param s3_hook: the s3 hook to make the operations with
        :type s3_hook: S3Hook
        :param path: the filepath to clean up
        :type path: str
        """
        self.log.info(f"fpath to clean up: {path}")
        try:
            objects_to_delete = s3_hook.list_keys(
                bucket_name=self.s3_bucket, prefix=path
            )
            self.log.info(f"objects to delete: {objects_to_delete}")
            s3_hook.delete_objects(bucket=self.s3_bucket, keys=objects_to_delete)
            return True
        except Exception:
            self.log.info(f"Cleanup of partition {path} failed")
            return False

    @staticmethod
    def get_random_string(char_count: int = 10) -> str:
        """
        Given number of characters returns a random string with that length.

        :param char_count: number of characters
        :type char_count: int
        """
        return "".join(
            random.choice(string.ascii_letters + string.digits)
            for _ in range(char_count)
        )

    @property
    def _target_file_path(self) -> str:
        """Get target blob path for the file.

        Returns:
            str: The target blob path for the file.
        """
        if not self.partitioned:
            if not self.s3_key.endswith(self.file_options.suffix):
                return (
                    f"{self._s3_key_prefix}/{BatchSqlToS3Operator.DEFAULT_PARTITION}/"
                )
            else:
                return f"{self.s3_key}"
        else:
            return f"{self._s3_key_prefix}/{self._partition}/"

    @property
    def _folder_to_clean(self) -> str:
        self.log.info(f"folder to clean s3_key_prefix {self._s3_key_prefix}")
        if not self.partitioned:
            folder_to_clean_up = f"{self._s3_key_prefix}/"
        else:
            folder_to_clean_up = f"{self._s3_key_prefix}/{self._partition}/"
        return folder_to_clean_up

    @property
    def partitioned(self) -> bool:
        """Check if the file is partitioned."""
        if self.where_clause:
            return True
        return False

    @property
    def _s3_key_prefix(self) -> str:
        return self.s3_key.rsplit("/", 1)[0]

    @property
    def _partition(self) -> str:
        return self.s3_key.rsplit("/", 1)[1]

    @property
    def file_options(self) -> FileOptions:
        """Get the file options for the file format."""
        return FILE_OPTIONS_MAP[self.file_format]

    def get_file_path(self) -> StoragePaths:
        """Get the file path and name for the file to be written.

        Returns:
            StoragePaths: The path and name of the file to be written.
        """
        if not self.partitioned:
            _path = self._s3_key_prefix + "/"
            _file = self.s3_key.rsplit("/", 1)[1]
            return {"path": _path, "file": _file}
        random_suffix = self.get_random_string(12)
        new_file_name = f"{random_suffix}{self.file_options.suffix}"
        new_file_path = f"{self._target_file_path}"
        return {"path": new_file_path, "file": new_file_name}

    def execute(self, context: Context) -> None:
        """Overwrite execute method of superclass to encompass complex behaviour."""
        print(f"LOG LEVEL: {self.log.level=}")
        self.query = self._create_select_query()
        self.log.info("::group::Query")
        self.log.info(text(self.query))
        self.log.info("::endgroup::")

        s3_conn = S3Hook(aws_conn_id=self.aws_conn_id, verify=self.verify)

        if self.replace:
            self.cleanup_s3_folder(s3_hook=s3_conn, path=self._folder_to_clean)

        first_run = True
        for df in self.get_pandas_data(sql=self.query):
            if df.empty:  # no point in writing files with no data
                self.log.info("No data from SQL obtained")
            else:
                self.log.info("Data from SQL obtained")

                if self.format_needed is True:
                    self._fix_dtypes(df, self.file_format)

                storage = self.get_file_path()

                self.xcom_push(context, key="target_file_path", value=storage["path"])
                self.xcom_push(context, key="target_file", value=storage["file"])
                self.xcom_push(context, key="partitioned", value=self.partitioned)

                self.log.info(f"is this rendered?: {self.s3_key}")
                self.log.info(f"New filepath: {storage['path']}")

                with NamedTemporaryFile(
                    mode=self.file_options.mode, suffix=self.file_options.suffix
                ) as tmp_file:
                    self.log.info("Writing data to temp file")
                    getattr(df, self.file_options.function)(
                        tmp_file.name, **self.pd_kwargs
                    )

                    if first_run:
                        # Get schema and xcom only once
                        s = pq.read_schema(tmp_file.name)
                        redshift_map = {
                            k: pyarrow2redshift(v, "VARCHAR")
                            for k, v in zip(s.names, s.types)
                        }
                        self.xcom_push(context, key="type_map", value=redshift_map)
                        first_run = False

                    self.log.info("Uploading data to S3")
                    s3_conn.load_file(
                        filename=tmp_file.name,
                        key=storage["path"] + storage["file"],
                        bucket_name=self.s3_bucket,
                        replace=self.replace,
                    )
