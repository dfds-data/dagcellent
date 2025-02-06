"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import TYPE_CHECKING

from airflow.hooks.base import BaseHook
from airflow.providers.openlineage.extractors.base import OperatorLineage
from airflow.typing_compat import TypedDict
from airflow.utils.log.logging_mixin import LoggingMixin
from attrs import define
from openlineage.client.event_v2 import Dataset
from openlineage.common.sql import DbTableMeta, SqlMeta
from sqlalchemy.engine import Engine

if TYPE_CHECKING: ...
DEFAULT_NAMESPACE = ...
DEFAULT_INFORMATION_SCHEMA_COLUMNS = ...
DEFAULT_INFORMATION_SCHEMA_TABLE_NAME = ...

def default_normalize_name_method(name: str) -> str: ...

class GetTableSchemasParams(TypedDict):
    """get_table_schemas params."""

    normalize_name: Callable[[str], str]
    is_cross_db: bool
    information_schema_columns: list[str]
    information_schema_table: str
    use_flat_cross_db_query: bool
    is_uppercase_names: bool
    database: str | None
    ...

@define
class DatabaseInfo:
    """
    Contains database specific information needed to process SQL statement parse result.

    :param scheme: Scheme part of URI in OpenLineage namespace.
    :param authority: Authority part of URI in OpenLineage namespace.
        For most cases it should return `{host}:{port}` part of Airflow connection.
        See: https://github.com/OpenLineage/OpenLineage/blob/main/spec/Naming.md
    :param database: Takes precedence over parsed database name.
    :param information_schema_columns: List of columns names from information schema table.
    :param information_schema_table_name: Information schema table name.
    :param use_flat_cross_db_query: Specifies if single information schema table should be used
        for cross-database queries (e.g. for Redshift).
    :param is_information_schema_cross_db: Specifies if information schema contains
        cross-database data.
    :param is_uppercase_names: Specifies if database accepts only uppercase names (e.g. Snowflake).
    :param normalize_name_method: Method to normalize database, schema and table names.
        Defaults to `name.lower()`.
    """

    scheme: str
    authority: str | None = ...
    database: str | None = ...
    information_schema_columns: list[str] = ...
    information_schema_table_name: str = ...
    use_flat_cross_db_query: bool = ...
    is_information_schema_cross_db: bool = ...
    is_uppercase_names: bool = ...
    normalize_name_method: Callable[[str], str] = ...

def from_table_meta(
    table_meta: DbTableMeta, database: str | None, namespace: str, is_uppercase: bool
) -> Dataset: ...

class SQLParser(LoggingMixin):
    """
    Interface for openlineage-sql.

    :param dialect: dialect specific to the database
    :param default_schema: schema applied to each table with no schema parsed
    """

    def __init__(
        self, dialect: str | None = ..., default_schema: str | None = ...
    ) -> None: ...
    def parse(self, sql: list[str] | str) -> SqlMeta | None:
        """Parse a single or a list of SQL statements."""
        ...

    def parse_table_schemas(
        self,
        hook: BaseHook,
        inputs: list[DbTableMeta],
        outputs: list[DbTableMeta],
        database_info: DatabaseInfo,
        namespace: str = ...,
        database: str | None = ...,
        sqlalchemy_engine: Engine | None = ...,
    ) -> tuple[list[Dataset], ...]:
        """Parse schemas for input and output tables."""
        ...

    def get_metadata_from_parser(
        self,
        inputs: list[DbTableMeta],
        outputs: list[DbTableMeta],
        database_info: DatabaseInfo,
        namespace: str = ...,
        database: str | None = ...,
    ) -> tuple[list[Dataset], ...]: ...
    def attach_column_lineage(
        self, datasets: list[Dataset], database: str | None, parse_result: SqlMeta
    ) -> None:
        """
        Attaches column lineage facet to the list of datasets.

        Note that currently each dataset has the same column lineage information set.
        This would be a matter of change after OpenLineage SQL Parser improvements.
        """
        ...

    def generate_openlineage_metadata_from_sql(
        self,
        sql: list[str] | str,
        hook: BaseHook,
        database_info: DatabaseInfo,
        database: str | None = ...,
        sqlalchemy_engine: Engine | None = ...,
        use_connection: bool = ...,
    ) -> OperatorLineage:
        """
        Parse SQL statement(s) and generate OpenLineage metadata.

        Generated OpenLineage metadata contains:

        * input tables with schemas parsed
        * output tables with schemas parsed
        * run facets
        * job facets.

        :param sql: a SQL statement or list of SQL statement to be parsed
        :param hook: Airflow Hook used to connect to the database
        :param database_info: database specific information
        :param database: when passed it takes precedence over parsed database name
        :param sqlalchemy_engine: when passed, engine's dialect is used to compile SQL queries
        """
        ...

    @staticmethod
    def create_namespace(database_info: DatabaseInfo) -> str: ...
    @classmethod
    def normalize_sql(cls, sql: list[str] | str) -> str:
        """Make sure to return a semicolon-separated SQL statement."""
        ...

    @classmethod
    def split_sql_string(cls, sql: list[str] | str) -> list[str]:
        """
        Split SQL string into list of statements.

        Tries to use `DbApiHook.split_sql_string` if available.
        Otherwise, uses the same logic.
        """
        ...

    def create_information_schema_query(
        self,
        tables: list[DbTableMeta],
        normalize_name: Callable[[str], str],
        is_cross_db: bool,
        information_schema_columns: list[str],
        information_schema_table: str,
        is_uppercase_names: bool,
        use_flat_cross_db_query: bool,
        database: str | None = ...,
        sqlalchemy_engine: Engine | None = ...,
    ) -> str:
        """Create SELECT statement to query information schema table."""
        ...
