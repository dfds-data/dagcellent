"""
This type stub file was generated by pyright.
"""

from typing import TYPE_CHECKING, Any

import flask
from connexion import ProblemException

if TYPE_CHECKING: ...
doc_link = ...
EXCEPTIONS_LINK_MAP = ...

def common_error_handler(exception: BaseException) -> flask.Response:
    """Use to capture connexion exceptions and add link to the type field."""
    ...

class NotFound(ProblemException):
    """Raise when the object cannot be found."""

    def __init__(
        self,
        title: str = ...,
        detail: str | None = ...,
        headers: dict | None = ...,
        **kwargs: Any,
    ) -> None: ...

class BadRequest(ProblemException):
    """Raise when the server processes a bad request."""

    def __init__(
        self,
        title: str = ...,
        detail: str | None = ...,
        headers: dict | None = ...,
        **kwargs: Any,
    ) -> None: ...

class Unauthenticated(ProblemException):
    """Raise when the user is not authenticated."""

    def __init__(
        self,
        title: str = ...,
        detail: str | None = ...,
        headers: dict | None = ...,
        **kwargs: Any,
    ) -> None: ...

class PermissionDenied(ProblemException):
    """Raise when the user does not have the required permissions."""

    def __init__(
        self,
        title: str = ...,
        detail: str | None = ...,
        headers: dict | None = ...,
        **kwargs: Any,
    ) -> None: ...

class AlreadyExists(ProblemException):
    """Raise when the object already exists."""

    def __init__(
        self,
        title=...,
        detail: str | None = ...,
        headers: dict | None = ...,
        **kwargs: Any,
    ) -> None: ...

class Unknown(ProblemException):
    """Returns a response body and status code for HTTP 500 exception."""

    def __init__(
        self,
        title: str = ...,
        detail: str | None = ...,
        headers: dict | None = ...,
        **kwargs: Any,
    ) -> None: ...
