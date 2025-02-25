"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, Any

from airflow.models.base import Base
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.session import provide_session
from sqlalchemy.orm import Session, declared_attr, reconstructor

if TYPE_CHECKING: ...
log = ...

class Variable(Base, LoggingMixin):
    """A generic way to store and retrieve arbitrary content or settings as a simple key/value store."""

    __tablename__ = ...
    __NO_DEFAULT_SENTINEL = ...
    id = ...
    key = ...
    _val = ...
    description = ...
    is_encrypted = ...
    def __init__(self, key=..., val=..., description=...) -> None: ...
    @reconstructor
    def on_db_load(self):  # -> None:
        ...
    def __repr__(self):  # -> str:
        ...
    def get_val(self):  # -> None:
        """Get Airflow Variable from Metadata DB and decode it using the Fernet Key."""
        ...

    def set_val(self, value):  # -> None:
        """Encode the specified value with Fernet Key and store it in Variables Table."""
        ...

    @declared_attr
    def val(cls):
        """Get Airflow Variable from Metadata DB and decode it using the Fernet Key."""
        ...

    @classmethod
    def setdefault(cls, key, default, description=..., deserialize_json=...):  # -> Any:
        """
        Return the current value for a key or store the default value and return it.

        Works the same as the Python builtin dict object.

        :param key: Dict key for this Variable
        :param default: Default value to set and return if the variable
            isn't already in the DB
        :param description: Default value to set Description of the Variable
        :param deserialize_json: Store this as a JSON encoded value in the DB
            and un-encode it when retrieving a value
        :param session: Session
        :return: Mixed
        """
        ...

    @classmethod
    def get(cls, key: str, default_var: Any = ..., deserialize_json: bool = ...) -> Any:
        """
        Get a value for an Airflow Variable Key.

        :param key: Variable Key
        :param default_var: Default value of the Variable if the Variable doesn't exist
        :param deserialize_json: Deserialize the value to a Python dict
        """
        ...

    @staticmethod
    @provide_session
    def set(
        key: str,
        value: Any,
        description: str | None = ...,
        serialize_json: bool = ...,
        session: Session = ...,
    ) -> None:
        """
        Set a value for an Airflow Variable with a given Key.

        This operation overwrites an existing variable.

        :param key: Variable Key
        :param value: Value to set for the Variable
        :param description: Description of the Variable
        :param serialize_json: Serialize the value to a JSON string
        :param session: Session
        """
        ...

    @staticmethod
    @provide_session
    def update(
        key: str, value: Any, serialize_json: bool = ..., session: Session = ...
    ) -> None:
        """
        Update a given Airflow Variable with the Provided value.

        :param key: Variable Key
        :param value: Value to set for the Variable
        :param serialize_json: Serialize the value to a JSON string
        :param session: Session
        """
        ...

    @staticmethod
    @provide_session
    def delete(key: str, session: Session = ...) -> int:
        """
        Delete an Airflow Variable for a given key.

        :param key: Variable Keys
        """
        ...

    def rotate_fernet_key(self):  # -> None:
        """Rotate Fernet Key."""
        ...

    @staticmethod
    def check_for_write_conflict(key: str) -> None:
        """
        Log a warning if a variable exists outside the metastore.

        If we try to write a variable to the metastore while the same key
        exists in an environment variable or custom secrets backend, then
        subsequent reads will not read the set value.

        :param key: Variable Key
        """
        ...

    @staticmethod
    def get_variable_from_secrets(key: str) -> str | None:
        """
        Get Airflow Variable by iterating over all Secret Backends.

        :param key: Variable Key
        :return: Variable Value
        """
        ...
