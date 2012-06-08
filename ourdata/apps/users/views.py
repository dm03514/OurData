from ourdata.apps.users.models import APICredentials, User

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


@view_config(route_name='add_credentials', request_method='POST', 
             permission='users')
def add_credentials(request):
    """Create api credentials for a user for a specific dataset."""

    # get the user
    try:
        user = User.objects.get(id=request.matchdict['user_id'])
    except User.DoesNotExist:
        raise Exception('User not found for id: %s' % 
                            (request.matchdict['user_id']))

    # get the dataset
    try:
        dataset = DatasetSchema.objects.get(id=request.matchdict['dataset_id'])
    except DatasetSchema.DoesNotExist:
        raise Exception('Dataset not found for id: %s' % 
                            (request.matchdict['dataset_id']))
       
    credentials = APICredentials()
    credential.generate_credentials(
        user_id=user.id, 
        dataset_name=dataset.title, 
        salt=request.registry.settings['auth.salt']
    ) 

    user.api_credentials.append(credentials)
    return {}
