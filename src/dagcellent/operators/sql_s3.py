from __future__ import annotations

import random
import string
from collections.abc import Iterable, Sequence
from typing import TYPE_CHECKING, Any, NamedTuple, TypedDict

from airflow.models.connection import Connection
from airflow.providers.amazon.aws.transfers.sql_to_s3 import (
    FILE_FORMAT,
    NamedTemporaryFile,
    S3Hook,
    SqlToS3Operator as AWSSqlToS3Operator,
)

from dagcellent._connection import ConnectionType

if TYPE_CHECKING:
    import pandas as pd
    from airflow.utils.context import Context
    from sqlalchemy.engine import Engine

from pyarrow import parquet as pq

from dagcellent.data_utils.sql_reflection import (
    Pyarrow2redshift,
    PyarrowMapping,
    safe_add_database_to_connection,
)


class FileOptions(NamedTuple):
    """Redefine class for type-hinting."""

    mode: str
    suffix: str
    function: str


FILE_OPTIONS_MAP = {
    FILE_FORMAT.CSV: FileOptions("r+", ".csv", "to_csv"),
    FILE_FORMAT.JSON: FileOptions("r+", ".json", "to_json"),
    FILE_FORMAT.PARQUET: FileOptions("rb+", ".parquet", "to_parquet"),
}


class StoragePaths(TypedDict):
    """Cloud blob storage path and full file name."""

    path: str
    file: str


class SqlToS3Operator(AWSSqlToS3Operator):
    """Move data from SQL source to S3.

    Uses batching. Empty files are not written, which prevents breaking external
    tables in Redshift.

    Partitioning
    If the data is partitioned, `run_date=` partitions will be used.

    Until we have observability, we will not optimize/move away from the
    built-in provider (and pandas).

    kwargs:
        aws_conn_id: reference to a specific S3 connection
        sql_conn_id: reference to a specific database.

    Example:
        Output query:

        ```sql
        SELECT [EngineSourceKey]
              ,[EngineSourceCode]
              ,[EngineSourceName]
        FROM [dbo].[t_D_EngineSource];
        ```
    """

    template_fields: Sequence[str] = (
        "database",
        "s3_bucket",
        "s3_key",
        "query",
        "sql_conn_id",
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
        chunksize: int = 10**6,
        fix_dtypes: bool = True,
        where_clause: str | None = None,
        join_clause: str | None = None,
        type_mapping: PyarrowMapping = Pyarrow2redshift,
        database: str | None = None,
        **kwargs: Any,
    ) -> None:  # type: ignore
        """Override constructor with extra chunksize argument."""
        super().__init__(**kwargs)  # type: ignore[UnknownTypeMember]
        if kwargs.get("query", None):
            self.log.info("%s", f"Query: {kwargs['query']}")
        self.chunksize = chunksize
        self.fix_dtypes = fix_dtypes
        self.database = database
        self.where_clause = where_clause
        self.join_clause = join_clause
        self.type_mapping = type_mapping

    def _supported_source_connections(self) -> list[str]:
        conn = Connection.get_connection_from_secrects(self.sql_conn_id)
        match conn.conn_type:
            case ConnectionType.MSSQL:
                return [ConnectionType.MSSQL]
            case ConnectionType.POSTGRES:
                return [ConnectionType.POSTGRES]
            case _:
                raise ValueError("Unsupported connection type.")

    def _sql_hook_with_db(self) -> Engine:
        """Add self.database to SQLAlchemy engine if it is not None."""
        sql_hook = self._get_hook()
        engine = sql_hook.get_sqlalchemy_engine()  # type: ignore
        if self.database is None:
            return engine
        # inject database name if not defined in connection URI
        # This works, but cannot cross query/reflect properly
        return safe_add_database_to_connection(engine, self.database)

    def _get_pandas_data(self, sql: str) -> Iterable[pd.DataFrame]:
        import pandas.io.sql as panda_sql

        engine = self._sql_hook_with_db()

        # NOTE pd type annotations are not strict enough
        with engine.connect() as conn:  # type: ignore
            yield from panda_sql.read_sql(  # type: ignore
                sql,
                con=conn,
                params=self.params,
                chunksize=self.chunksize,  # type: ignore
            )

    def _clean_s3_folder(self, s3_hook: S3Hook, path: str) -> bool:
        """Delete the objects in the s3 folder.

        Args:
            s3_hook: the s3 hook to make the operations with
            path: the file path to clean up

        Returns:
            bool: True if the cleanup was successful
        """
        self.log.debug("%s", f"fpath to clean up: {path}")
        try:
            objects_to_delete = s3_hook.list_keys(  # type: ignore
                bucket_name=self.s3_bucket, prefix=path
            )
            self.log.debug("%s", f"Objects to delete: {objects_to_delete}")
            s3_hook.delete_objects(bucket=self.s3_bucket, keys=objects_to_delete)  # type: ignore[ReportUnknownArgumentType]
            return True
        except Exception:
            self.log.debug("%s", f"Cleanup of partition {path} failed")
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
            str: the target path for the file
        """
        if not self.partitioned:
            if not self.s3_key.endswith(self.file_options.suffix):
                return f"{self._s3_key_prefix}/{SqlToS3Operator.DEFAULT_PARTITION}/"
            else:
                return f"{self.s3_key}"
        else:
            return f"{self._s3_key_prefix}/{self._partition}/"

    @property
    def _folder_to_clean(self) -> str:
        self.log.info("%s", f"folder to clean s3_key_prefix {self._s3_key_prefix}")
        if not self.partitioned:
            folder_to_clean_up = f"{self._s3_key_prefix}/"
        else:
            folder_to_clean_up = f"{self._s3_key_prefix}/{self._partition}/"
        return folder_to_clean_up

    @property
    def partitioned(self) -> bool:
        """Check if the file is partitioned.

        Returns:
            bool: True if the file is partitioned
        """
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

    def _get_file_path(self) -> StoragePaths:
        """Get the file path and name for the file to be written.

        Returns:
            StoragePaths: the path and name of the file to be written.
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
        """Logic of the operator."""
        print(f"log level: {self.log.level=}")

        s3_conn = S3Hook(aws_conn_id=self.aws_conn_id, verify=self.verify)

        if self.replace:
            self._clean_s3_folder(s3_hook=s3_conn, path=self._folder_to_clean)

        first_run = True
        for df in self._get_pandas_data(sql=self.query):
            # Empty df is not written to S3
            if df.empty:
                self.log.warning("Empty dataframe, skipping.")
                continue

            if self.fix_dtypes is True:
                self._fix_dtypes(df, self.file_format)

            storage = self._get_file_path()

            # Only push xcoms once
            if first_run:
                self.log.info("%s", f"New filepath: {storage['path']}")
                self.xcom_push(context, key="target_file_path", value=storage["path"])
                self.xcom_push(context, key="target_file", value=storage["file"])
                self.xcom_push(context, key="partitioned", value=self.partitioned)

            with NamedTemporaryFile(
                mode=self.file_options.mode, suffix=self.file_options.suffix
            ) as tmp_file:
                self.log.info("Writing data to temp file")
                getattr(df, self.file_options.function)(
                    tmp_file.name,
                    **self.pd_kwargs,  # type: ignore
                )

                if first_run:
                    # Get schema and xcom only once
                    # NOTE pyarrow did not type hint the read_schema method
                    s = pq.read_schema(tmp_file.name)  # type: ignore[UnknownTypeMember]
                    _mapped_type = {  # type: ignore[UnknownTypeMember]
                        k: self.type_mapping.map(v, "VARCHAR")  # type: ignore[no-untyped-call]
                        for k, v in zip(s.names, s.types)  # type: ignore[no-untyped-call]
                    }
                    self.xcom_push(context, key="type_map", value=_mapped_type)
                    first_run = False

                self.log.info("Uploading data to S3")
                s3_conn.load_file(  # type: ignore[UnknownTypeMember]
                    filename=tmp_file.name,
                    key=storage["path"] + storage["file"],
                    bucket_name=self.s3_bucket,
                    replace=self.replace,
                )
