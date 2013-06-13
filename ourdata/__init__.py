from ourdata.apps.users.models import User
from ourdata.apps.apis.views import APIAuthFieldGetRequest
from mongoengine import connect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated, Deny, unauthenticated_userid


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(
        settings=settings,
        root_factory=Root
    )
    config.add_static_view('static', 'static', cache_max_age=3600)

    # views.apis
    config.add_route('api_field_get', '/api/{dataset_slug}/{field_name}/get')
    config.add_view(APIAuthFieldGetRequest)

    # views.datasets
    config.add_route('dataset_create', '/dataset/create')
    config.add_route('dataset_get', '/dataset/get/{slug}')
    config.add_route('column_create', '/dataset/{slug}/column/create')

    # views.pages
    config.add_route('home', '/')
    config.add_route('signup', '/signup')
    config.add_route('dashboard', '/dashboard')
    config.add_route('dashboard_admin', '/dashboard/admin')
    config.add_route('test', '/test')

    # views.users
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('add_credentials', '/user/credentials/add/{user_id}')
    config.add_route('edit_permissions', '/user/permissions/edit/{user_id}')


    #import ipdb; ipdb.set_trace()
    authn_policy = AuthTktAuthenticationPolicy(settings['auth.salt'], 
        callback=group_finder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    connect(settings['mongo_db_name'])

    config.set_request_property(get_user, 'user', reify=True)

    config.scan()
    return config.make_wsgi_app()

def group_finder(user_id, request):
    """
    Find an active user's groups for a request.
    """
    try:
        user = User.objects.get(id=user_id)
        return user.groups
    except User.DoesNotExist:
        pass

def get_user(request):
    """
    See if the current user is logged in and fetch the corresponding
    user object.
    """
    user_id = unauthenticated_userid(request)
    if user_id is not None:
        return User.objects.get(id=user_id, is_active=True)


class Root(object):
    """Contains all acl for all groups."""
    __acl__ = [
        (Allow, 'admin', ALL_PERMISSIONS),
    ]
    #http://docs.pylonsproject.org/projects/pyramid/en/latest/tutorials/wiki/authorization.html

    def __init__(self, request):
        self.request = request
