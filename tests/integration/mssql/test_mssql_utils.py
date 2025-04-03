from __future__ import annotations

from typing import TYPE_CHECKING

from dagcellent.data_utils.sql_reflection import reflect_meta_data

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


def test_reflect_meta_data(db_engine: Engine):
    table = reflect_meta_data(db_engine, schema="dbo", table="test")
    assert table is not None
    assert table.name == "test"
