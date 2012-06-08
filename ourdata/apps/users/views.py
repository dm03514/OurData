from ourdata.apps.users.models import User

from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid, remember, forget
from pyramid.view import view_config

@view_config(route_name='login', request_method='POST')
def login(request):
    """Log a user in check their credentials"""
    required_params_list = ['email', 'password']
    for param in required_params_list:
        if not request.POST.get(param):
            raise Exception('Param: %s missing from request' % 
                            (param))
    
    user = User.authenticate(request.POST['email'], 
                             request.POST['password'])
    if user is None:
        raise Exception('Invalid Credentials')

    headers = remember(request, str(user.id))
    return HTTPFound(location='dashboard', headers=headers)

@view_config(route_name='logout', request_method='GET')
def logout(request):
    """Log a user out by forgetting cookies"""
    return HTTPFound(location='/', headers=forget(request))


@view_config(route_name='add_credentials', request_method='POST')
def add_credentials(request):
    raise Exception('Not Implemented')
