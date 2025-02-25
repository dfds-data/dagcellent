"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING

import packaging.version
from airflow import __version__ as airflow_version
from airflow.auth.managers.models.base_user import BaseUser
from flask_appbuilder.models.sqla import Model
from sqlalchemy import event
from sqlalchemy.orm import declared_attr

if TYPE_CHECKING: ...
metadata = ...
mapper_registry = ...
if packaging.version.parse(
    packaging.version.parse(airflow_version).base_version
) >= packaging.version.parse("3.0.0"): ...
else: ...

class Action(Model):
    """Represents permission actions such as `can_read`."""

    __tablename__ = ...
    id = ...
    name = ...
    def __repr__(self): ...

class Resource(Model):
    """Represents permission object such as `User` or `Dag`."""

    __tablename__ = ...
    id = ...
    name = ...
    def __eq__(self, other) -> bool: ...
    def __neq__(self, other): ...
    def __repr__(self): ...

assoc_permission_role = ...

class Role(Model):
    """Represents a user role to which permissions can be assigned."""

    __tablename__ = ...
    id = ...
    name = ...
    permissions = ...
    def __repr__(self): ...

class Permission(Model):
    """Permission pair comprised of an Action + Resource combo."""

    __tablename__ = ...
    __table_args__ = ...
    id = ...
    action_id = ...
    action = ...
    resource_id = ...
    resource = ...
    def __repr__(self):  # -> str:
        ...

assoc_user_role = ...

class User(Model, BaseUser):
    """Represents an Airflow user which has roles assigned to it."""

    __tablename__ = ...
    id = ...
    first_name = ...
    last_name = ...
    username = ...
    password = ...
    active = ...
    email = ...
    last_login = ...
    login_count = ...
    fail_login_count = ...
    roles = ...
    created_on = ...
    changed_on = ...
    @declared_attr
    def created_by_fk(self):  # -> Column:
        ...
    @declared_attr
    def changed_by_fk(self):  # -> Column:
        ...

    created_by = ...
    changed_by = ...
    @classmethod
    def get_user_id(cls):  # -> Any | None:
        ...
    @property
    def is_authenticated(self):  # -> Literal[True]:
        ...
    @property
    def is_active(self): ...
    @property
    def is_anonymous(self):  # -> Literal[False]:
        ...
    @property
    def perms(self):  # -> set[tuple[str, str]]:
        ...
    def get_id(self): ...
    def get_name(self) -> str: ...
    def get_full_name(self):  # -> str:
        ...
    def __repr__(self):  # -> str:
        ...

    _perms = ...

class RegisterUser(Model):
    """Represents a user registration."""

    __tablename__ = ...
    id = ...
    first_name = ...
    last_name = ...
    username = ...
    password = ...
    email = ...
    registration_date = ...
    registration_hash = ...

@event.listens_for(User.__table__, "before_create")
def add_index_on_ab_user_username_postgres(table, conn, **kw):  # -> None:
    ...
@event.listens_for(RegisterUser.__table__, "before_create")
def add_index_on_ab_register_user_username_postgres(table, conn, **kw):  # -> None:
    ...
