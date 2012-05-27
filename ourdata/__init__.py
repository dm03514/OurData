from mongoengine import connect
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # views.pages
    config.add_route('home', '/')
    config.add_route('signup', '/signup')
    config.add_route('dashboard', '/dashboard')

    # views.users
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    authn_policy = AuthTktAuthenticationPolicy('sosecret')
    authz_policy = ACLAuthorizationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    connect(settings['mongo_db_name'])
    config.scan()
    return config.make_wsgi_app()
