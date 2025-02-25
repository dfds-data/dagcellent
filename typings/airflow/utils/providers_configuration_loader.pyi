"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable
from typing import TypeVar

from airflow.typing_compat import ParamSpec

PS = ParamSpec("PS")
RT = TypeVar("RT")

def providers_configuration_loaded(func: Callable[PS, RT]) -> Callable[PS, RT]:
    """
    Make sure that providers configuration is loaded before actually calling the decorated function.

    ProvidersManager initialization of configuration is relatively inexpensive - it walks through
    all providers's entrypoints, retrieve the provider_info and loads config yaml parts of the get_info.
    Unlike initialization of hooks and operators it does not import any of the provider's code, so it can
    be run quickly by all commands that need to access providers configuration. We cannot even import
    ProvidersManager while importing any of the commands, so we need to locally import it here.

    We cannot initialize the configuration in settings/conf because of the way how conf/settings are used
    internally - they are loaded while importing airflow, and we need to access airflow version conf in the
    ProvidesManager initialization, so instead we opt for decorating all the methods that need it with this
    decorator.

    The decorator should be placed below @suppress_logs_and_warning but above @provide_session in order to
    avoid spoiling the output of formatted options with some warnings ar infos, and to be prepared that
    session creation might need some configuration defaults from the providers configuration.

    :param func: function to makes sure that providers configuration is loaded before actually calling
    """
    ...
