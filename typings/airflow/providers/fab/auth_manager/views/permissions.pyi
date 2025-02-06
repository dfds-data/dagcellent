"""
This type stub file was generated by pyright.
"""

from flask_appbuilder.security.views import (
    PermissionModelView,
    PermissionViewModelView,
    ViewMenuModelView,
)

class ActionModelView(PermissionModelView):
    """Customize permission names for FAB's builtin PermissionModelView."""

    class_permission_name = ...
    route_base = ...
    method_permission_name = ...
    base_permissions = ...
    list_title = ...
    show_title = ...
    add_title = ...
    edit_title = ...
    label_columns = ...

class PermissionPairModelView(PermissionViewModelView):
    """Customize permission names for FAB's builtin PermissionViewModelView."""

    class_permission_name = ...
    route_base = ...
    method_permission_name = ...
    base_permissions = ...
    list_title = ...
    show_title = ...
    add_title = ...
    edit_title = ...
    label_columns = ...
    list_columns = ...

class ResourceModelView(ViewMenuModelView):
    """Customize permission names for FAB's builtin ViewMenuModelView."""

    class_permission_name = ...
    route_base = ...
    method_permission_name = ...
    base_permissions = ...
    list_title = ...
    show_title = ...
    add_title = ...
    edit_title = ...
    label_columns = ...
