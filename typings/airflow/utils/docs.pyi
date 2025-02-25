"""
This type stub file was generated by pyright.
"""

import sys

if sys.version_info >= (3, 10): ...
else: ...

def get_docs_url(page: str | None = ...) -> str:
    """Prepare link to Airflow documentation."""
    ...

def get_project_url_from_metadata(provider_name: str):  # -> list[Any] | None:
    """Return the Project-URL from metadata."""
    ...

def get_doc_url_for_provider(provider_name: str, provider_version: str) -> str:
    """Prepare link to Airflow Provider documentation."""
    ...
