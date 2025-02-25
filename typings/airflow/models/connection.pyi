"""
This type stub file was generated by pyright.
"""

from typing import Any

from airflow.models.base import Base
from airflow.utils.log.logging_mixin import LoggingMixin
from sqlalchemy.orm import declared_attr, reconstructor

log = ...
RE_SANITIZE_CONN_ID = ...
CONN_ID_MAX_LEN: int = ...

def parse_netloc_to_hostname(*args, **kwargs):  # -> str:
    """Do not use, this method is deprecated."""
    ...

def sanitize_conn_id(conn_id: str | None, max_length=...) -> str | None:
    r"""
    Sanitizes the connection id and allows only specific characters to be within.

    Namely, it allows alphanumeric characters plus the symbols #,!,-,_,.,:,\,/ and () from 1 and up to
    250 consecutive matches. If desired, the max length can be adjusted by setting `max_length`.

    You can try to play with the regex here: https://regex101.com/r/69033B/1

    The character selection is such that it prevents the injection of javascript or
    executable bits to avoid any awkward behaviour in the front-end.

    :param conn_id: The connection id to sanitize.
    :param max_length: The max length of the connection ID, by default it is 250.
    :return: the sanitized string, `None` otherwise.
    """
    ...

class Connection(Base, LoggingMixin):
    """
    Placeholder to store information about different database instances connection information.

    The idea here is that scripts use references to database instances (conn_id)
    instead of hard coding hostname, logins and passwords when using operators or hooks.

    .. seealso::
        For more information on how to use this class, see: :doc:`/howto/connection`

    :param conn_id: The connection ID.
    :param conn_type: The connection type.
    :param description: The connection description.
    :param host: The host.
    :param login: The login.
    :param password: The password.
    :param schema: The schema.
    :param port: The port number.
    :param extra: Extra metadata. Non-standard data such as private/SSH keys can be saved here. JSON
        encoded object.
    :param uri: URI address describing connection parameters.
    """

    EXTRA_KEY = ...
    __tablename__ = ...
    id = ...
    conn_id = ...
    conn_type = ...
    description = ...
    host = ...
    schema = ...
    login = ...
    _password = ...
    port = ...
    is_encrypted = ...
    is_extra_encrypted = ...
    _extra = ...
    def __init__(
        self,
        conn_id: str | None = ...,
        conn_type: str | None = ...,
        description: str | None = ...,
        host: str | None = ...,
        login: str | None = ...,
        password: str | None = ...,
        schema: str | None = ...,
        port: int | None = ...,
        extra: str | dict | None = ...,
        uri: str | None = ...,
    ) -> None: ...
    @reconstructor
    def on_db_load(self):  # -> None:
        ...
    def parse_from_uri(self, **uri):  # -> None:
        """Use uri parameter in constructor, this method is deprecated."""
        ...

    def get_uri(self) -> str:
        """Return connection in URI format."""
        ...

    def get_password(self) -> str | None:
        """Return encrypted password."""
        ...

    def set_password(self, value: str | None):  # -> None:
        """Encrypt password and set in object attribute."""
        ...

    @declared_attr
    def password(cls):
        """Password. The value is decrypted/encrypted when reading/setting the value."""
        ...

    def get_extra(self) -> str:
        """Return encrypted extra-data."""
        ...

    def set_extra(self, value: str):  # -> None:
        """Encrypt extra-data and save in object attribute to object."""
        ...

    @declared_attr
    def extra(cls):
        """Extra data. The value is decrypted/encrypted when reading/setting the value."""
        ...

    def rotate_fernet_key(self):  # -> None:
        """Encrypts data with a new key. See: :ref:`security/fernet`."""
        ...

    def get_hook(self, *, hook_params=...):  # -> Any:
        """Return hook based on conn_type."""
        ...

    def __repr__(self):  # -> str:
        ...
    def log_info(self):  # -> str:
        """
        Read each field individually or use the default representation (`__repr__`).

        This method is deprecated.
        """
        ...

    def debug_info(self):  # -> str:
        """
        Read each field individually or use the default representation (`__repr__`).

        This method is deprecated.
        """
        ...

    def test_connection(self):  # -> tuple[Any | Literal[False], Any | str]:
        """Calls out get_hook method and executes test_connection method on that."""
        ...

    def get_extra_dejson(self, nested: bool = ...) -> dict:
        """
        Deserialize extra property to JSON.

        :param nested: Determines whether nested structures are also deserialized into JSON (default False).
        """
        ...

    @property
    def extra_dejson(self) -> dict:
        """Returns the extra property by deserializing json."""
        ...

    @classmethod
    def get_connection_from_secrets(cls, conn_id: str) -> Connection:
        """
        Get connection by conn_id.

        :param conn_id: connection id
        :return: connection
        """
        ...

    def to_dict(
        self, *, prune_empty: bool = ..., validate: bool = ...
    ) -> dict[str, Any]:
        """
        Convert Connection to json-serializable dictionary.

        :param prune_empty: Whether or not remove empty values.
        :param validate: Validate dictionary is JSON-serializable

        :meta private:
        """
        ...

    @classmethod
    def from_json(cls, value, conn_id=...) -> Connection: ...
    def as_json(self) -> str:
        """Convert Connection to JSON-string object."""
        ...
