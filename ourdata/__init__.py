from mongoengine import connect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.security import ALL_PERMISSIONS, Allow, Authenticated, Deny


def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(
        settings=settings,
        root_factory=Root
    )
    config.add_static_view('static', 'static', cache_max_age=3600)

    # views.pages
    config.add_route('home', '/')
    config.add_route('signup', '/signup')
    config.add_route('dashboard', '/dashboard')

    # views.users
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    # views.datasets
    config.add_route('dataset_create', '/dataset/create')

    authn_policy = AuthTktAuthenticationPolicy('sosecret',
                    callback=group_finder)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    connect(settings['mongo_db_name'])
    config.scan()
    return config.make_wsgi_app()

def group_finder(user_id, request):
    """
    Find a user's groups for a request.
    """
    try:
        user = User.objects.get(id=user_id)
        return [group for group in user.groups]
    except User.DoesNotExist:
        pass


class Root(object):
    """Contains all acl for all groups."""
    __acl__ = [
        (Allow, 'admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request
