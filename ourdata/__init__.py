from mongoengine import connect
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    # views.website.py
    config.add_route('home', '/')
    config.add_route('signup', '/signup')

    connect(settings['mongo_db_name'])
    config.scan()
    return config.make_wsgi_app()
