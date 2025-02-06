"""
This type stub file was generated by pyright.
"""

from airflow.auth.managers.models.base_user import BaseUser
from flask_login import AnonymousUserMixin

class AnonymousUser(AnonymousUserMixin, BaseUser):
    """User object used when no active user is logged in."""

    _roles: set[tuple[str, str]] = ...
    _perms: set[tuple[str, str]] = ...
    first_name = ...
    last_name = ...
    @property
    def roles(self):  # -> set[tuple[str, str]]:
        ...
    @roles.setter
    def roles(self, roles):  # -> None:
        ...
    @property
    def perms(self):  # -> set[tuple[str, str]]:
        ...
    def get_name(self) -> str: ...
