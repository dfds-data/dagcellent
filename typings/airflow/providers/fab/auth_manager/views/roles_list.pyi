"""
This type stub file was generated by pyright.
"""

from flask_appbuilder.security.views import RoleModelView

class CustomRoleModelView(RoleModelView):
    """Customize permission names for FAB's builtin RoleModelView."""

    class_permission_name = ...
    method_permission_name = ...
    base_permissions = ...
