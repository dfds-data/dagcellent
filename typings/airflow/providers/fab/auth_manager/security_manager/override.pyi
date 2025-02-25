"""
This type stub file was generated by pyright.
"""

from collections.abc import Callable, Collection, Container, Iterable, Mapping, Sequence
from typing import (
    TYPE_CHECKING,
    Any,
)

import packaging.version
from airflow import __version__ as airflow_version
from airflow.exceptions import AirflowProviderDeprecationWarning
from airflow.models import DagModel
from airflow.providers.fab.auth_manager.models import (
    Action,
    Permission,
    RegisterUser,
    Resource,
    Role,
    User,
)
from airflow.providers.fab.auth_manager.views.permissions import (
    ActionModelView,
    PermissionPairModelView,
    ResourceModelView,
)
from airflow.providers.fab.auth_manager.views.roles_list import CustomRoleModelView
from airflow.providers.fab.auth_manager.views.user import (
    CustomUserDBModelView,
    CustomUserLDAPModelView,
    CustomUserOAuthModelView,
    CustomUserOIDModelView,
    CustomUserRemoteUserModelView,
)
from airflow.providers.fab.auth_manager.views.user_edit import (
    CustomResetMyPasswordView,
    CustomResetPasswordView,
    CustomUserInfoEditView,
)
from airflow.providers.fab.auth_manager.views.user_stats import CustomUserStatsChartView
from airflow.security import permissions
from airflow.utils.session import provide_session
from airflow.www.security_manager import AirflowSecurityManagerV2
from deprecated import deprecated
from flask_appbuilder.security.registerviews import (
    RegisterUserDBView,
    RegisterUserOAuthView,
    RegisterUserOIDView,
)
from flask_appbuilder.security.views import (
    AuthDBView,
    AuthLDAPView,
    AuthOAuthView,
    AuthOIDView,
    AuthRemoteUserView,
    AuthView,
    RegisterUserModelView,
)
from flask_appbuilder.views import expose
from flask_login import LoginManager
from sqlalchemy.orm import Session

if TYPE_CHECKING: ...
else: ...
log = ...
MAX_NUM_DATABASE_USER_SESSIONS = ...
if packaging.version.parse(
    packaging.version.parse(airflow_version).base_version
) < packaging.version.parse("2.10.0"):
    _methods = ...
else:
    _methods = ...

class _ModifiedAuthView(AuthView):
    @expose("/logout/", methods=_methods)
    def logout(self):  # -> Response:
        ...

class FabAirflowSecurityManagerOverride(AirflowSecurityManagerV2):
    """
    This security manager overrides the default AirflowSecurityManager security manager.

    This security manager is used only if the auth manager FabAuthManager is used. It defines everything in
    the security manager that is needed for the FabAuthManager to work. Any operation specific to
    the AirflowSecurityManager should be defined here instead of AirflowSecurityManager.

    :param appbuilder: The appbuilder.
    """

    auth_view = ...
    registeruser_view = ...
    user_view = ...
    user_model = User
    role_model = Role
    action_model = Action
    resource_model = Resource
    permission_model = Permission
    authdbview = AuthDBView
    authldapview = AuthLDAPView
    authoidview = AuthOIDView
    authoauthview = AuthOAuthView
    authremoteuserview = AuthRemoteUserView
    registeruserdbview = RegisterUserDBView
    registeruseroidview = RegisterUserOIDView
    registeruseroauthview = RegisterUserOAuthView
    actionmodelview = ActionModelView
    permissionmodelview = PermissionPairModelView
    rolemodelview = CustomRoleModelView
    registeruser_model = RegisterUser
    registerusermodelview = RegisterUserModelView
    resourcemodelview = ResourceModelView
    userdbmodelview = CustomUserDBModelView
    resetmypasswordview = CustomResetMyPasswordView
    resetpasswordview = CustomResetPasswordView
    userinfoeditview = CustomUserInfoEditView
    userldapmodelview = CustomUserLDAPModelView
    useroauthmodelview = CustomUserOAuthModelView
    userremoteusermodelview = CustomUserRemoteUserModelView
    useroidmodelview = CustomUserOIDModelView
    userstatschartview = CustomUserStatsChartView
    jwt_manager = ...
    oid = ...
    oauth = ...
    oauth_remotes: dict[str, Any]
    oauth_user_info = ...
    oauth_allow_list: dict[str, list] = ...
    DAG_RESOURCES = ...
    VIEWER_PERMISSIONS = ...
    USER_PERMISSIONS = ...
    OP_PERMISSIONS = ...
    ADMIN_PERMISSIONS = ...
    ROLE_CONFIGS: list[dict[str, Any]] = ...
    RESOURCE_DETAILS_MAP = ...
    DAG_ACTIONS = RESOURCE_DETAILS_MAP[permissions.RESOURCE_DAG]["actions"]
    def __init__(self, appbuilder) -> None: ...
    def register_views(self):  # -> None:
        """Register FAB auth manager related views."""
        ...

    @property
    def get_session(self): ...
    def create_login_manager(self) -> LoginManager:
        """Create the login manager."""
        ...

    def create_jwt_manager(self):  # -> None:
        """Create the JWT manager."""
        ...

    def reset_password(self, userid: int, password: str) -> bool:
        """
        Change/Reset a user's password for auth db.

        Password will be hashed and saved.

        :param userid: the user id to reset the password
        :param password: the clear text password to reset and save hashed on the db
        """
        ...

    def reset_user_sessions(self, user: User) -> None: ...
    def load_user_jwt(self, _jwt_header, jwt_data):  # -> None:
        ...
    @property
    def auth_type(self):
        """Get the auth type."""
        ...

    @property
    def is_auth_limited(self) -> bool:
        """Is the auth rate limited."""
        ...

    @property
    def auth_rate_limit(self) -> str:
        """Get the auth rate limit."""
        ...

    @property
    def auth_role_public(self):
        """Get the public role."""
        ...

    @property
    def oauth_providers(self):
        """Oauth providers."""
        ...

    @property
    def auth_ldap_tls_cacertdir(self):
        """LDAP TLS CA certificate directory."""
        ...

    @property
    def auth_ldap_tls_cacertfile(self):
        """LDAP TLS CA certificate file."""
        ...

    @property
    def auth_ldap_tls_certfile(self):
        """LDAP TLS certificate file."""
        ...

    @property
    def auth_ldap_tls_keyfile(self):
        """LDAP TLS key file."""
        ...

    @property
    def auth_ldap_allow_self_signed(self):
        """LDAP allow self signed."""
        ...

    @property
    def auth_ldap_tls_demand(self):
        """LDAP TLS demand."""
        ...

    @property
    def auth_ldap_server(self):
        """Get the LDAP server object."""
        ...

    @property
    def auth_ldap_use_tls(self):
        """Should LDAP use TLS."""
        ...

    @property
    def auth_ldap_bind_user(self):
        """LDAP bind user."""
        ...

    @property
    def auth_ldap_bind_password(self):
        """LDAP bind password."""
        ...

    @property
    def auth_ldap_search(self):
        """LDAP search object."""
        ...

    @property
    def auth_ldap_search_filter(self):
        """LDAP search filter."""
        ...

    @property
    def auth_ldap_uid_field(self):
        """LDAP UID field."""
        ...

    @property
    def auth_ldap_firstname_field(self):
        """LDAP first name field."""
        ...

    @property
    def auth_ldap_lastname_field(self):
        """LDAP last name field."""
        ...

    @property
    def auth_ldap_email_field(self):
        """LDAP email field."""
        ...

    @property
    def auth_ldap_append_domain(self):
        """LDAP append domain."""
        ...

    @property
    def auth_ldap_username_format(self):
        """LDAP username format."""
        ...

    @property
    def auth_ldap_group_field(self) -> str:
        """LDAP group field."""
        ...

    @property
    def auth_roles_mapping(self) -> dict[str, list[str]]:
        """The mapping of auth roles."""
        ...

    @property
    def auth_user_registration_role_jmespath(self) -> str:
        """The JMESPATH role to use for user registration."""
        ...

    @property
    def auth_remote_user_env_var(self) -> str: ...
    @property
    def api_login_allow_multiple_providers(self): ...
    @property
    def auth_username_ci(self):
        """Get the auth username for CI."""
        ...

    @property
    def auth_ldap_bind_first(self):
        """LDAP bind first."""
        ...

    @property
    def openid_providers(self):
        """Openid providers."""
        ...

    @property
    def auth_type_provider_name(self):  # -> str | None:
        ...
    @property
    def auth_user_registration(self):
        """Will user self registration be allowed."""
        ...

    @property
    def auth_user_registration_role(self):
        """The default user self registration role."""
        ...

    @property
    def auth_roles_sync_at_login(self) -> bool:
        """Should roles be synced at login."""
        ...

    @property
    def auth_role_admin(self):
        """Get the admin role."""
        ...

    @property
    @deprecated(
        reason="The 'oauth_whitelists' property is deprecated. Please use 'oauth_allow_list' instead.",
        category=AirflowProviderDeprecationWarning,
    )
    def oauth_whitelists(self):  # -> dict[str, list[Any]]:
        ...
    def create_builtin_roles(self):
        """Return FAB builtin roles."""
        ...

    @property
    def builtin_roles(self):  # -> dict[Any, Any]:
        """Get the builtin roles."""
        ...

    def create_admin_standalone(self) -> tuple[str | None, str | None]:
        """Create an Admin user with a random password so that users can access airflow."""
        ...

    def create_db(self):  # -> None:
        """
        Create the database.

        Creates admin and public roles if they don't exist.
        """
        ...

    def get_readable_dags(self, user) -> Iterable[DagModel]:
        """Get the DAGs readable by authenticated user."""
        ...

    def get_editable_dags(self, user) -> Iterable[DagModel]:
        """Get the DAGs editable by authenticated user."""
        ...

    @provide_session
    def get_accessible_dags(
        self, user_actions: Container[str] | None, user, session: Session = ...
    ) -> Iterable[DagModel]: ...
    @provide_session
    def get_accessible_dag_ids(
        self, user, user_actions: Container[str] | None = ..., session: Session = ...
    ) -> set[str]: ...
    @staticmethod
    def get_readable_dag_ids(user=...) -> set[str]:
        """Get the DAG IDs readable by authenticated user."""
        ...

    @staticmethod
    def get_editable_dag_ids(user=...) -> set[str]:
        """Get the DAG IDs editable by authenticated user."""
        ...

    def can_access_some_dags(self, action: str, dag_id: str | None = ...) -> bool:
        """Check if user has read or write access to some dags."""
        ...

    def get_all_permissions(self) -> set[tuple[str, str]]:
        """Return all permissions as a set of tuples with the action and resource names."""
        ...

    def create_dag_specific_permissions(self) -> None:
        """
        Add permissions to all DAGs.

        Creates 'can_read', 'can_edit', and 'can_delete' permissions for all
        DAGs, along with any `access_control` permissions provided in them.

        This does iterate through ALL the DAGs, which can be slow. See `sync_perm_for_dag`
        if you only need to sync a single DAG.
        """
        ...

    def prefixed_dag_id(self, dag_id: str) -> str:
        """Return the permission name for a DAG id."""
        ...

    def is_dag_resource(self, resource_name: str) -> bool:
        """Determine if a resource belongs to a DAG or all DAGs."""
        ...

    def sync_perm_for_dag(
        self,
        dag_id: str,
        access_control: Mapping[str, Mapping[str, Collection[str]] | Collection[str]]
        | None = ...,
    ) -> None:
        """
        Sync permissions for given dag id.

        The dag id surely exists in our dag bag as only / refresh button or DagBag will call this function.

        :param dag_id: the ID of the DAG whose permissions should be updated
        :param access_control: a dict where each key is a role name and each value can be:
             - a set() of DAGs resource action names (e.g. `{'can_read'}`)
             - or a dict where each key is a resource name ('DAGs' or 'DAG Runs') and each value
             is a set() of action names (e.g., `{'DAG Runs': {'can_create'}, 'DAGs': {'can_read'}}`)
        :return:
        """
        ...

    def add_permissions_view(self, base_action_names, resource_name):  # -> None:
        """
        Add an action on a resource to the backend.

        :param base_action_names:
            list of permissions from view (all exposed methods):
             'can_add','can_edit' etc...
        :param resource_name:
            name of the resource to add
        """
        ...

    def add_permissions_menu(self, resource_name):  # -> None:
        """
        Add menu_access to resource on permission_resource.

        :param resource_name:
            The resource name
        """
        ...

    def security_cleanup(self, baseviews, menus):  # -> None:
        """
        Cleanup all unused permissions from the database.

        :param baseviews: A list of BaseViews class
        :param menus: Menu class
        """
        ...

    def sync_roles(self) -> None:
        """
        Initialize default and custom roles with related permissions.

        1. Init the default role(Admin, Viewer, User, Op, public)
           with related permissions.
        2. Init the custom role(dag-user) with related permissions.
        """
        ...

    def create_perm_vm_for_all_dag(self) -> None:
        """Create perm-vm if not exist and insert into FAB security model for all-dags."""
        ...

    def add_homepage_access_to_custom_roles(self) -> None:
        """Add Website.can_read access to all custom roles."""
        ...

    def update_admin_permission(self) -> None:
        """
        Add missing permissions to the table for admin.

        Admin should get all the permissions, except the dag permissions
        because Admin already has Dags permission.
        Add the missing ones to the table for admin.
        """
        ...

    def clean_perms(self) -> None:
        """FAB leaves faulty permissions that need to be cleaned up."""
        ...

    def permission_exists_in_one_or_more_roles(
        self, resource_name: str, action_name: str, role_ids: list[int]
    ) -> bool:
        """
        Efficiently check if a certain permission exists on a list of role ids; used by `has_access`.

        :param resource_name: The view's name to check if exists on one of the roles
        :param action_name: The permission name to check if exists
        :param role_ids: a list of Role ids
        :return: Boolean
        """
        ...

    def perms_include_action(self, perms, action_name):  # -> bool:
        ...
    def init_role(self, role_name, perms) -> None:
        """
        Initialize the role with actions and related resources.

        :param role_name:
        :param perms:
        """
        ...

    def bulk_sync_roles(self, roles: Iterable[dict[str, Any]]) -> None:
        """Sync the provided roles and permissions."""
        ...

    def sync_resource_permissions(
        self, perms: Iterable[tuple[str, str]] | None = ...
    ) -> None:
        """Populate resource-based permissions."""
        ...

    def update_role(self, role_id, name: str) -> Role | None:
        """Update a role in the database."""
        ...

    def add_role(self, name: str) -> Role:
        """Add a role in the database."""
        ...

    def find_role(self, name):
        """
        Find a role in the database.

        :param name: the role name
        """
        ...

    def get_all_roles(self): ...
    def delete_role(self, role_name: str) -> None:
        """
        Delete the given Role.

        :param role_name: the name of a role in the ab_role table
        """
        ...

    def get_roles_from_keys(self, role_keys: list[str]) -> set[Role]:
        """
        Construct a list of FAB role objects, from a list of keys.

        NOTE:
        - keys are things like: "LDAP group DNs" or "OAUTH group names"
        - we use AUTH_ROLES_MAPPING to map from keys, to FAB role names

        :param role_keys: the list of FAB role keys
        """
        ...

    def get_public_role(self): ...
    def add_user(
        self,
        username,
        first_name,
        last_name,
        email,
        role,
        password=...,
        hashed_password=...,
    ):  # -> User | Literal[False]:
        """Create a user."""
        ...

    def load_user(self, user_id):  # -> None:
        ...
    def get_user_by_id(self, pk): ...
    def count_users(self):
        """Return the number of users in the database."""
        ...

    def add_register_user(
        self, username, first_name, last_name, email, password=..., hashed_password=...
    ):  # -> RegisterUser | None:
        """
        Add a registration request for the user.

        :rtype : RegisterUser
        """
        ...

    def find_user(self, username=..., email=...):  # -> None:
        """Find user by username or email."""
        ...

    def find_register_user(self, registration_hash): ...
    def update_user(self, user: User) -> bool: ...
    def del_register_user(self, register_user):  # -> bool:
        """
        Delete registration object from database.

        :param register_user: RegisterUser object to delete
        """
        ...

    def get_all_users(self): ...
    def update_user_auth_stat(self, user, success=...):  # -> None:
        """
        Update user authentication stats.

        This is done upon successful/unsuccessful authentication attempts.

        :param user:
            The identified (but possibly not successfully authenticated) user
            model
        :param success:
            Defaults to true, if true increments login_count, updates
            last_login, and resets fail_login_count to 0, if false increments
            fail_login_count on user model.
        """
        ...

    def get_action(self, name: str) -> Action:
        """
        Get an existing action record.

        :param name: name
        """
        ...

    def create_action(self, name):  # -> Action:
        """
        Add an action to the backend, model action.

        :param name:
            name of the action: 'can_add','can_edit' etc...
        """
        ...

    def delete_action(self, name: str) -> bool:
        """
        Delete a permission action.

        :param name: Name of action to delete (e.g. can_read).
        """
        ...

    def get_resource(self, name: str) -> Resource:
        """
        Return a resource record by name, if it exists.

        :param name: Name of resource
        """
        ...

    def create_resource(self, name) -> Resource:
        """
        Create a resource with the given name.

        :param name: The name of the resource to create created.
        """
        ...

    def get_all_resources(self) -> list[Resource]:
        """Get all existing resource records."""
        ...

    def delete_resource(self, name: str) -> bool:
        """
        Delete a Resource from the backend.

        :param name:
            name of the resource
        """
        ...

    def get_permission(self, action_name: str, resource_name: str) -> Permission | None:
        """
        Get a permission made with the given action->resource pair, if the permission already exists.

        :param action_name: Name of action
        :param resource_name: Name of resource
        """
        ...

    def get_resource_permissions(self, resource: Resource) -> Permission:
        """
        Retrieve permission pairs associated with a specific resource object.

        :param resource: Object representing a single resource.
        """
        ...

    def create_permission(self, action_name, resource_name) -> Permission | None:
        """
        Add a permission on a resource to the backend.

        :param action_name:
            name of the action to add: 'can_add','can_edit' etc...
        :param resource_name:
            name of the resource to add
        """
        ...

    def delete_permission(self, action_name: str, resource_name: str) -> None:
        """
        Delete the permission linking an action->resource pair.

        Doesn't delete the underlying action or resource.

        :param action_name: Name of existing action
        :param resource_name: Name of existing resource
        """
        ...

    def add_permission_to_role(self, role: Role, permission: Permission | None) -> None:
        """
        Add an existing permission pair to a role.

        :param role: The role about to get a new permission.
        :param permission: The permission pair to add to a role.
        """
        ...

    def remove_permission_from_role(self, role: Role, permission: Permission) -> None:
        """
        Remove a permission pair from a role.

        :param role: User role containing permissions.
        :param permission: Object representing resource-> action pair
        """
        ...

    def get_oid_identity_url(self, provider_name: str) -> str | None:
        """Return the OIDC identity provider URL."""
        ...

    @staticmethod
    def get_user_roles(user=...):  # -> Any:
        """
        Get all the roles associated with the user.

        :param user: the ab_user in FAB model.
        :return: a list of roles associated with the user.
        """
        ...

    def auth_user_ldap(self, username, password):
        """
        Authenticate user with LDAP.

        NOTE: this depends on python-ldap module.

        :param username: the username
        :param password: the password
        """
        ...

    def auth_user_db(self, username, password):  # -> None:
        """
        Authenticate user, auth db style.

        :param username:
            The username or registered email address
        :param password:
            The password, will be tested against hashed password on db
        """
        ...

    def oauth_user_info_getter(
        self,
        func: Callable[
            [AirflowSecurityManagerV2, str, dict[str, Any] | None], dict[str, Any]
        ],
    ):  # -> Callable[..., dict[str, Any]]:
        """
        Get OAuth user info for all the providers.

        Receives provider and response return a dict with the information returned from the provider.
        The returned user info dict should have its keys with the same name as the User Model.

        Use it like this an example for GitHub ::

            @appbuilder.sm.oauth_user_info_getter
            def my_oauth_user_info(sm, provider, response=None):
                if provider == "github":
                    me = sm.oauth_remotes[provider].get("user")
                    return {"username": me.data.get("login")}
                return {}
        """
        ...

    def get_oauth_user_info(
        self, provider: str, resp: dict[str, Any]
    ) -> dict[str, Any]:
        """
        There are different OAuth APIs with different ways to retrieve user info.

        All providers have different ways to retrieve user info.
        """
        ...

    @staticmethod
    def oauth_token_getter():  # -> None:
        """Get authentication (OAuth) token."""
        ...

    def check_authorization(
        self, perms: Sequence[tuple[str, str]] | None = ..., dag_id: str | None = ...
    ) -> bool:
        """Check the logged-in user has the specified permissions."""
        ...

    def set_oauth_session(self, provider, oauth_response):  # -> None:
        """Set the current session with OAuth user secrets."""
        ...

    def get_oauth_token_key_name(self, provider):  # -> None:
        """
        Return the token_key name for the oauth provider.

        If none is configured defaults to oauth_token
        this is configured using OAUTH_PROVIDERS and token_key key.
        """
        ...

    def get_oauth_token_secret_name(self, provider):  # -> None:
        """
        Get the ``token_secret`` name for the oauth provider.

        If none is configured, defaults to ``oauth_secret``. This is configured
        using ``OAUTH_PROVIDERS`` and ``token_secret``.
        """
        ...

    def auth_user_oauth(self, userinfo):  # -> User | None:
        """
        Authenticate user with OAuth.

        :userinfo: dict with user information
                   (keys are the same as User model columns)
        """
        ...

    def auth_user_oid(self, email):  # -> None:
        """
        Openid user Authentication.

        :param email: user's email to authenticate
        """
        ...

    def auth_user_remote_user(self, username):  # -> User | Literal[False] | None:
        """
        REMOTE_USER user Authentication.

        :param username: user's username for remote auth
        """
        ...

    def get_user_menu_access(self, menu_names: list[str] | None = ...) -> set[str]: ...
    @staticmethod
    def ldap_extract_list(
        ldap_dict: dict[str, list[bytes]], field_name: str
    ) -> list[str]: ...
    @staticmethod
    def ldap_extract(
        ldap_dict: dict[str, list[bytes]], field_name: str, fallback: str
    ) -> str: ...
    def filter_roles_by_perm_with_action(self, action_name: str, role_ids: list[int]):
        """Find roles with permission."""
        ...
