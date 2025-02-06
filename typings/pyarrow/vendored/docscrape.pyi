"""
This type stub file was generated by pyright.
"""

from collections.abc import Mapping

"""Extract reference documentation from the NumPy source tree.

"""

def strip_blank_lines(l):
    "Remove leading and trailing blank lines from a list of lines"
    ...

class Reader:
    """A line-based string reader."""

    def __init__(self, data) -> None:
        """
        Parameters
        ----------
        data : str
           String with lines separated by '\\n'.

        """
        ...

    def __getitem__(self, n): ...
    def reset(self):  # -> None:
        ...
    def read(self):  # -> Literal['']:
        ...
    def seek_next_non_empty_line(self):  # -> None:
        ...
    def eof(self):  # -> bool:
        ...
    def read_to_condition(self, condition_func):  # -> list[Any]:
        ...
    def read_to_next_empty_line(self):  # -> list[Any]:
        ...
    def read_to_next_unindented_line(self):  # -> list[Any]:
        ...
    def peek(self, n=...):  # -> Literal['']:
        ...
    def is_empty(self):  # -> bool:
        ...

class ParseError(Exception):
    def __str__(self) -> str: ...

Parameter = ...

class NumpyDocString(Mapping):
    """Parses a numpydoc string to an abstract representation

    Instances define a mapping from section title to structured data.

    """

    sections = ...
    def __init__(self, docstring, config=...) -> None: ...
    def __getitem__(self, key): ...
    def __setitem__(self, key, val):  # -> None:
        ...
    def __iter__(self):  # -> Iterator[str]:
        ...
    def __len__(self):  # -> int:
        ...

    _role = ...
    _funcbacktick = ...
    _funcplain = ...
    _funcname = ...
    _funcnamenext = ...
    _funcnamenext = ...
    _description = ...
    _func_rgx = ...
    _line_rgx = ...
    empty_description = ...
    def __str__(self, func_role=...) -> str: ...

def dedent_lines(lines):  # -> list[str]:
    """Deindent a list of lines maximally"""
    ...

class FunctionDoc(NumpyDocString):
    def __init__(self, func, role=..., doc=..., config=...) -> None: ...
    def get_func(self):  # -> tuple[Any | Callable[..., Any], Any | str]:
        ...
    def __str__(self) -> str: ...

class ObjDoc(NumpyDocString):
    def __init__(self, obj, doc=..., config=...) -> None: ...

class ClassDoc(NumpyDocString):
    extra_public_methods = ...
    def __init__(
        self, cls, doc=..., modulename=..., func_doc=..., config=...
    ) -> None: ...
    @property
    def methods(self):  # -> list[Any] | list[str]:
        ...
    @property
    def properties(self):  # -> list[Any] | list[str]:
        ...

def get_doc_object(
    obj, what=..., doc=..., config=...
):  # -> ClassDoc | FunctionDoc | ObjDoc:
    ...
