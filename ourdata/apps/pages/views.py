from ourdata.apps.common.exceptions import UserExists
from ourdata.apps.users.models import User

from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid, remember
from pyramid.view import view_config

@view_config(route_name='home', renderer='ourdata:templates/home.pt')
def home(request):
    """Render the home template"""
    return {'project':'OurData'}

@view_config(route_name='signup', request_method='GET',
             renderer='ourdata:templates/signup.pt')
def signup_get(request):
    """Render signup template"""
    return {}

@view_config(route_name='signup', request_method='POST')
def signup_post(request):
    """
    Process a request to sign a user up.  Returns errors or a
    redirect on success
    """
    required_params_list = ['first_name', 'last_name', 'email', 
                            'password']
    for param in required_params_list:
        if not request.POST.get(param):
            raise Exception('Param: %s missing from request' % 
                            (param))
    # check if user exists based on email
    new_user = User.create_user(request.POST['email'],
        request.POST['first_name'], request.POST['last_name'],
        request.POST['password'])

    # log user in and redirect
    headers = remember(request, str(new_user.id))
    return HTTPFound(location='dashboard', headers=headers)

@view_config(route_name='dashboard', request_method='GET', 
            renderer='ourdata:templates/dashboard.pt')
def dashboard(request):
    """Render the dashboard template"""
    user_id = authenticated_userid(request)
    if user_id is None:
        raise Exception('Unauthenticated User!')
    return {}
