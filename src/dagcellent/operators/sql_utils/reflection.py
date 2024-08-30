from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING, TypeAlias

import pyarrow as pa
from sqlalchemy import MetaData, create_engine, create_mock_engine, select
from sqlalchemy.dialects.mssql.base import UNIQUEIDENTIFIER
from sqlalchemy.schema import Column, CreateTable, Table


class UnsupportedType(Exception):
    """Unsupported type exception."""

    pass


if TYPE_CHECKING:
    from sqlalchemy.engine import Engine

Query: TypeAlias = str


def pyarrow2redshift(dtype: pa.DataType, string_type: str) -> str:
    """Pyarrow to Redshift data types conversion."""
    if pa.types.is_int8(dtype):
        return "SMALLINT"
    if pa.types.is_int16(dtype) or pa.types.is_uint8(dtype):
        return "SMALLINT"
    if pa.types.is_int32(dtype) or pa.types.is_uint16(dtype):
        return "INTEGER"
    if pa.types.is_int64(dtype) or pa.types.is_uint32(dtype):
        return "BIGINT"
    if pa.types.is_uint64(dtype):
        raise UnsupportedType(
            "There is no support for uint64, please consider int64 or uint32."
        )
    if pa.types.is_float32(dtype):
        return "FLOAT4"
    if pa.types.is_float64(dtype):
        return "FLOAT8"
    if pa.types.is_boolean(dtype):
        return "BOOL"
    if pa.types.is_string(dtype) or pa.types.is_large_string(dtype):
        return string_type
    if pa.types.is_timestamp(dtype):
        return "TIMESTAMP"
    if pa.types.is_date(dtype):
        return "DATE"
    if pa.types.is_time(dtype):
        return "TIME"
    if pa.types.is_binary(dtype):
        return "VARBYTE"
    if pa.types.is_decimal(dtype):
        return f"DECIMAL({dtype.precision},{dtype.scale})"
    if pa.types.is_dictionary(dtype):
        return pyarrow2redshift(dtype=dtype.value_type, string_type=string_type)
    if pa.types.is_list(dtype) or pa.types.is_struct(dtype) or pa.types.is_map(dtype):
        return "SUPER"
    raise UnsupportedType(f"Unsupported Redshift type: {dtype}")


def drop_unsupported_dtypes(table: Table) -> Table:
    _dummy_meta_data = MetaData()
    good_columns: list[Column] = []
    for col in table.columns.values():
        match col.type:
            case UNIQUEIDENTIFIER():
                warnings.warn(
                    f"Column {col.name} is of type UNIQUEIDENTIFIER, which is not supported."
                    " Column is not selected from the table.",
                    stacklevel=1,
                )
                continue
            case _:
                # None of the unsupported datatypes are met.
                good_columns.append(Column(col.name, col.type))

    _dummy_table = Table(table.name, _dummy_meta_data, *good_columns)
    _dummy_table.schema = table.schema
    return _dummy_table


def reflect_select_query(table: Table, engine: Engine) -> Query:
    """Reflects the select query from the metadata."""
    table = drop_unsupported_dtypes(table)
    return str(select([table]).compile(engine))


def reflect_meta_data(engine: Engine) -> MetaData:
    """Reflects the metadata from the engine."""
    meta_data = MetaData()
    meta_data.reflect(bind=engine)
    return meta_data


def _log_reflected_table(meta_data: MetaData, table_name: str) -> None:
    """Debug utility: Logs the reflected table."""
    for c in meta_data.tables[table_name].columns:  # type: ignore
        logging.info(f"{c.name: <15} {c.type!s: <15}")


def strip_table_constraints(table: Table) -> Table:
    """Returns a dummy Table object with only columns, types, precision, and scale."""
    _dummy_meta_data = MetaData()
    _dummy_table = Table(
        table.name, _dummy_meta_data, *[Column(c.name, c.type) for c in table.columns]
    )
    return _dummy_table


def create_external_table_redshift(
    table: Table,
    s3_location: str,
    partitioned: bool = False,
    dialect: str = "redshift://",
    schema_name: str | None = None,
) -> Query:
    if schema_name:
        table.schema = schema_name
    mock = create_mock_engine(dialect, executor=lambda *args: None)
    query = f"{CreateTable(table).compile(dialect=mock.dialect)!s}"
    query = _external_table_query_redshift(query, s3_location, partitioned=partitioned)
    return query


def create_external_table_redshift_arrow(
    type_map: dict[str, str],
    table: str,
    s3_location: str,
    partitioned: bool = False,
    dialect: str = "redshift://",
    schema_name: str | None = None,
) -> tuple[Query, Query | None]:
    query = "".join([f"  {k} {v},\n" for k, v in type_map.items()])
    query = query.rstrip(",\n")
    query = f"CREATE EXTERNAL TABLE {schema_name}.{table} (\n" + query + "\n) "
    query = _external_table_query_redshift(query, s3_location, partitioned=partitioned)
    partition_query = None
    if partitioned:
        partition_query = _add_external_partition_redshift(
            table, schema_name, s3_location
        )
    return query, partition_query


def _add_external_partition_redshift(
    table: str, schema_name: str, s3_location: str
) -> Query:
    """Add a partition to an external table in Redshift.

    [docs](https://docs.aws.amazon.com/redshift/latest/dg/r_ALTER_TABLE_external-table.html)
    """
    run_date = s3_location.split("run_date=")[1].split("/")[0]
    partition = (
        f"ALTER TABLE {schema_name}.{table} "
        f"ADD IF NOT EXISTS PARTITION (run_date='{run_date}') "
        f"location '{s3_location}';"
    )
    return partition


def _external_table_query_redshift(
    q: Query, s3_location: str, partitioned: bool = False
) -> Query:
    """We only allow partitioning by run_date.

    Reference: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html.
    """
    q = q.replace("CREATE TABLE", "CREATE EXTERNAL TABLE")
    if partitioned:
        q += "PARTITIONED BY (run_date date)\n"
    q += "STORED AS PARQUET\n"
    if partitioned and "run_date=" in s3_location:
        s3_location = s3_location.split("run_date=")[0]
    q += f"LOCATION '{s3_location}'\n"
    q += "TABLE PROPERTIES ('classification'='parquet')"
    q += ";"
    return q


if __name__ == "__main__":
    import pandas as pd

    engine = create_engine("mssql+pymssql://sa:Alma1234@localhost:1433/master")
    table_name = "test"
    reflect_meta_data = reflect_meta_data(engine)
    target_table = reflect_meta_data.tables[table_name]  # type: ignore[attr-defined]

    # _log_reflected_table(reflect_meta_data, table_name)
    print("---")
    # print(reflect_select_query(target_table, engine))
    target_table = strip_table_constraints(target_table)
    # print(create_external_table_redshift(target_table, "s3://bucket/key"))
    query = reflect_select_query(target_table, engine)
    df = pd.read_sql(query, con=engine)

    df.to_parquet(
        "test.parquet",
        engine="pyarrow",
        **{"version": "2.6", "coerce_timestamps": "us"},
    )
