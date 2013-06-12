from pyramid.httpexceptions import HTTPFound, HTTPNotFound, HTTPClientError, HTTPMovedPermanently
from pyramid.security import authenticated_userid, remember, forget
from pyramid.view import view_config

from ourdata.apps.apis.models import APICredential
from ourdata.apps.datasets.models import DatasetSchema
from ourdata.apps.users.models import User

@view_config(route_name='edit_permissions', request_method='GET', 
             renderer='ourdata:templates/users/edit_permissions.mak',
             permission='users')
def edit_permissions(request):
    """
    Allows admin to edit permissions of a user
    """
    try:
        user = User.objects.get(id=request.matchdict['user_id'])
    except User.DoesNotExist:
        return HTTPNotFound();

    user_credentials = APICredential.objects.filter(user_id=request.matchdict['user_id']) 
    all_datasets = DatasetSchema.objects.all()

    return {
        'all_datasets': all_datasets,
        'user_credentials': user_credentials,
        'user_id': request.matchdict['user_id']    
    }


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
    dataset_id = request.POST.get('dataset_id')
    if not dataset_id:
        return HTTPClientError()

    # get the user
    try:
        user = User.objects.get(id=request.matchdict['user_id'])
    except User.DoesNotExist:
        return HTTPNotFound()

    # get the dataset
    try:
        dataset = DatasetSchema.objects.get(id=request.POST['dataset_id'])
    except DatasetSchema.DoesNotExist:
        return HTTPNotFound()

       
    APICredential.generate_credential(
        user_id=user.id, 
        dataset_obj=dataset, 
        salt=request.registry.settings['auth.salt']
    ) 

    return HTTPMovedPermanently(location=request.route_url('edit_permissions', 
                                                           user_id=request.matchdict['user_id']))
