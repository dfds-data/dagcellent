"""
This type stub file was generated by pyright.
"""

from flask_appbuilder import expose
from flask_appbuilder.security.decorators import has_access
from flask_appbuilder.security.views import (
    UserDBModelView,
    UserLDAPModelView,
    UserOAuthModelView,
    UserOIDModelView,
    UserRemoteUserModelView,
)

class MultiResourceUserMixin:
    """Remaps UserModelView permissions to new resources and actions."""

    _class_permission_name = ...
    class_permission_name_mapping = ...
    method_permission_name = ...
    base_permissions = ...
    @property
    def class_permission_name(self):  # -> str:
        """Returns appropriate permission name depending on request method name."""
        ...

    @class_permission_name.setter
    def class_permission_name(self, name):  # -> None:
        ...
    @expose("/show/<pk>", methods=["GET"])
    @has_access
    def show(self, pk): ...

class CustomUserLDAPModelView(MultiResourceUserMixin, UserLDAPModelView):
    """Customize permission names for FAB's builtin UserLDAPModelView."""

    _class_permission_name = ...
    class_permission_name_mapping = ...
    method_permission_name = ...
    base_permissions = ...

class CustomUserOAuthModelView(MultiResourceUserMixin, UserOAuthModelView):
    """Customize permission names for FAB's builtin UserOAuthModelView."""

    ...

class CustomUserOIDModelView(MultiResourceUserMixin, UserOIDModelView):
    """Customize permission names for FAB's builtin UserOIDModelView."""

    ...

class CustomUserRemoteUserModelView(MultiResourceUserMixin, UserRemoteUserModelView):
    """Customize permission names for FAB's builtin UserRemoteUserModelView."""

    _class_permission_name = ...
    class_permission_name_mapping = ...
    method_permission_name = ...
    base_permissions = ...

class CustomUserDBModelView(MultiResourceUserMixin, UserDBModelView):
    """Customize permission names for FAB's builtin UserDBModelView."""

    _class_permission_name = ...
    class_permission_name_mapping = ...
    method_permission_name = ...
    base_permissions = ...
