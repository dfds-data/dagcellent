"""
This type stub file was generated by pyright.
"""

import packaging.version
from airflow import __version__ as airflow_version

__all__ = ["__version__"]
__version__ = ...
if packaging.version.parse(
    packaging.version.parse(airflow_version).base_version
) < packaging.version.parse("2.9.0"): ...
