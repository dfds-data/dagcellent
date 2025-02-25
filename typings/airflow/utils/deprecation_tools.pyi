"""
This type stub file was generated by pyright.
"""

def getattr_with_deprecation(
    imports: dict[str, str],
    module: str,
    override_deprecated_classes: dict[str, str],
    extra_message: str,
    name: str,
):  # -> Any:
    """
    Retrieve the imported attribute from the redirected module and raises a deprecation warning.

    :param imports: dict of imports and their redirection for the module
    :param module: name of the module in the package to get the attribute from
    :param override_deprecated_classes: override target classes with deprecated ones. If target class is
       found in the dictionary, it will be displayed in the warning message.
    :param extra_message: extra message to display in the warning or import error message
    :param name: attribute name
    :return:
    """
    ...

def add_deprecated_classes(
    module_imports: dict[str, dict[str, str]],
    package: str,
    override_deprecated_classes: dict[str, dict[str, str]] | None = ...,
    extra_message: str | None = ...,
):  # -> None:
    """
    Add deprecated class PEP-563 imports and warnings modules to the package.

    :param module_imports: imports to use
    :param package: package name
    :param override_deprecated_classes: override target classes with deprecated ones. If module +
       target class is found in the dictionary, it will be displayed in the warning message.
    :param extra_message: extra message to display in the warning or import error message
    """
    ...
