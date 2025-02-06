"""
This type stub file was generated by pyright.
"""

from typing import Any, ClassVar

import attr

"""Defines base entities used for providing lineage information."""

@attr.s(auto_attribs=True)
class File:
    """File entity. Refers to a file."""

    template_fields: ClassVar = ...
    url: str = ...
    type_hint: str | None = ...

@attr.s(auto_attribs=True, kw_only=True)
class User:
    """User entity. Identifies a user."""

    email: str = ...
    first_name: str | None = ...
    last_name: str | None = ...
    template_fields: ClassVar = ...

@attr.s(auto_attribs=True, kw_only=True)
class Tag:
    """Tag or classification entity."""

    tag_name: str = ...
    template_fields: ClassVar = ...

@attr.s(auto_attribs=True, kw_only=True)
class Column:
    """Column of a Table."""

    name: str = ...
    description: str | None = ...
    data_type: str = ...
    tags: list[Tag] = ...
    template_fields: ClassVar = ...

def default_if_none(arg: bool | None) -> bool:
    """Get default value when None."""
    ...
@attr.s(auto_attribs=True, kw_only=True)
class Table:
    """Table entity."""

    database: str = ...
    cluster: str = ...
    name: str = ...
    tags: list[Tag] = ...
    description: str | None = ...
    columns: list[Column] = ...
    owners: list[User] = ...
    extra: dict[str, Any] = ...
    type_hint: str | None = ...
    template_fields: ClassVar = ...
