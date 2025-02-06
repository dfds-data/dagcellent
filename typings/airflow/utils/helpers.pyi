"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Generator, Iterable, Mapping, MutableMapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
)

import jinja2
from airflow.models.taskinstance import TaskInstance
from airflow.utils.context import Context

if TYPE_CHECKING: ...
KEY_REGEX = ...
GROUP_KEY_REGEX = ...
CAMELCASE_TO_SNAKE_CASE_REGEX = ...
T = TypeVar("T")
S = TypeVar("S")

def validate_key(k: str, max_length: int = ...):  # -> None:
    """Validate value used as a key."""
    ...

def validate_instance_args(
    instance: object, expected_arg_types: dict[str, Any]
) -> None:
    """Validate that the instance has the expected types for the arguments."""
    ...

def validate_group_key(k: str, max_length: int = ...):  # -> None:
    """Validate value used as a group key."""
    ...

def alchemy_to_dict(obj: Any) -> dict | None:
    """Transform a SQLAlchemy model instance into a dictionary."""
    ...

def ask_yesno(question: str, default: bool | None = ...) -> bool:
    """Get a yes or no answer from the user."""
    ...

def prompt_with_timeout(
    question: str, timeout: int, default: bool | None = ...
) -> bool:
    """Ask the user a question and timeout if they don't respond."""
    ...

def is_container(obj: Any) -> bool:
    """Test if an object is a container (iterable) but not a string."""
    ...

def as_tuple(obj: Any) -> tuple:
    """Return obj as a tuple if obj is a container, otherwise return a tuple containing obj."""
    ...

def chunks(items: list[T], chunk_size: int) -> Generator[list[T], None, None]:
    """Yield successive chunks of a given size from a list of items."""
    ...

def reduce_in_chunks(
    fn: Callable[[S, list[T]], S],
    iterable: list[T],
    initializer: S,
    chunk_size: int = ...,
):  # -> S:
    """Split the list of items into chunks of a given size and pass each chunk through the reducer."""
    ...

def as_flattened_list(iterable: Iterable[Iterable[T]]) -> list[T]:
    """
    Return an iterable with one level flattened.

    >>> as_flattened_list((("blue", "red"), ("green", "yellow", "pink")))
    ['blue', 'red', 'green', 'yellow', 'pink']
    """
    ...

def parse_template_string(
    template_string: str,
) -> tuple[str | None, jinja2.Template | None]:
    """Parse Jinja template string."""
    ...

def render_log_filename(ti: TaskInstance, try_number, filename_template) -> str:
    """
    Given task instance, try_number, filename_template, return the rendered log filename.

    :param ti: task instance
    :param try_number: try_number of the task
    :param filename_template: filename template, which can be jinja template or
        python string template
    """
    ...

def convert_camel_to_snake(camel_str: str) -> str:
    """Convert CamelCase to snake_case."""
    ...

def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Merge two dicts recursively, returning new dict (input dict is not mutated).

    Lists are not concatenated. Items in dict2 overwrite those also found in dict1.
    """
    ...

def partition(
    pred: Callable[[T], bool], iterable: Iterable[T]
) -> tuple[Iterable[T], Iterable[T]]:
    """Use a predicate to partition entries into false entries and true entries."""
    ...

def chain(*args, **kwargs):  # -> Any:
    """Use `airflow.models.baseoperator.chain`, this function is deprecated."""
    ...

def cross_downstream(*args, **kwargs):  # -> Any:
    """Use `airflow.models.baseoperator.cross_downstream`, this function is deprecated."""
    ...

def build_airflow_url_with_query(query: dict[str, Any]) -> str:
    """
    Build airflow url using base_url and default_view and provided query.

    For example:
    http://0.0.0.0:8000/base/graph?dag_id=my-task&root=&execution_date=2020-10-27T10%3A59%3A25.615587
    """
    ...

def render_template(
    template: Any, context: MutableMapping[str, Any], *, native: bool
) -> Any:
    """
    Render a Jinja2 template with given Airflow context.

    The default implementation of ``jinja2.Template.render()`` converts the
    input context into dict eagerly many times, which triggers deprecation
    messages in our custom context class. This takes the implementation apart
    and retain the context mapping without resolving instead.

    :param template: A Jinja2 template to render.
    :param context: The Airflow task context to render the template with.
    :param native: If set to *True*, render the template into a native type. A
        DAG can enable this with ``render_template_as_native_obj=True``.
    :returns: The render result.
    """
    ...

def render_template_to_string(template: jinja2.Template, context: Context) -> str:
    """Shorthand to ``render_template(native=False)`` with better typing support."""
    ...

def render_template_as_native(template: jinja2.Template, context: Context) -> Any:
    """Shorthand to ``render_template(native=True)`` with better typing support."""
    ...

def exactly_one(*args) -> bool:
    """
    Return True if exactly one of *args is "truthy", and False otherwise.

    If user supplies an iterable, we raise ValueError and force them to unpack.
    """
    ...

def at_most_one(*args) -> bool:
    """
    Return True if at most one of *args is "truthy", and False otherwise.

    NOTSET is treated the same as None.

    If user supplies an iterable, we raise ValueError and force them to unpack.
    """
    ...

def prune_dict(val: Any, mode=...):  # -> dict[Any, Any] | list[Any] | Any:
    """
    Given dict ``val``, returns new dict based on ``val`` with all empty elements removed.

    What constitutes "empty" is controlled by the ``mode`` parameter.  If mode is 'strict'
    then only ``None`` elements will be removed.  If mode is ``truthy``, then element ``x``
    will be removed if ``bool(x) is False``.
    """
    ...

def prevent_duplicates(
    kwargs1: dict[str, Any], kwargs2: Mapping[str, Any], *, fail_reason: str
) -> None:
    """
    Ensure *kwargs1* and *kwargs2* do not contain common keys.

    :raises TypeError: If common keys are found.
    """
    ...
