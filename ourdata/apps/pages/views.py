from ourdata.apps.common.exceptions import UserExists
from ourdata.apps.apis.models import APICredential
from ourdata.apps.users.models import User

from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid, remember
from pyramid.view import view_config

@view_config(route_name='home', renderer='ourdata:templates/home.mak')
def home(request):
    """Render the home template"""
    return {'project':'OurData'}

@view_config(route_name='signup', request_method='GET',
             renderer='ourdata:templates/signup.mak')
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
            renderer='ourdata:templates/dashboard.mak')
def dashboard(request):
    """Render the dashboard template"""
    # this allows any user to request so check that user has a
    # valid account

    #import ipdb; ipdb.set_trace()
    if request.user is None:
        raise Exception('User is not logged in')

    credential_params = {}
    # if user is admin get ALL credentials
    if not request.user.is_member_of('admin'):
        credential_params = {user_id: request.user.id}

    credentials = APICredential.objects.filter(**credential_params)

    # get all apis that this user belongs to 
    return {'credentials': credentials}


@view_config(route_name='test', renderer='ourdata:templates/examples.mak')
def test(request):
    return {}
