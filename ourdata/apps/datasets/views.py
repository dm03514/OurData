from datetime import datetime

from ourdata.apps.datasets.models import DatasetSchema, Field, VALID_DATA_TYPES
from ourdata.apps.users.models import User

from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.view import view_config


@view_config(
    route_name='column_create', 
    permission='datasets', 
    request_method='POST', 
    renderer='json',
)
def column_create(request):
    """
    Preforms Create a new column.
    """
    try:
        dataset = DatasetSchema.objects.get(
            slug=request.matchdict['slug']
        ) 
    except DatasetSchema.DoesNotExist:
        return {
            'success': False, 
            'message': 'No dataset named: %s' % 
                (request.matchdict['slug'])
        }
    # make sure required params are here
    required_params_list = ['name', 'data_type']
    for param in required_params_list:
        if not request.POST.get(param):
            return {
                'success': False, 
                'message': 'Param: %s missing from request' % (param),
            }

    name = request.POST['name']
    data_type = request.POST['data_type']

    # make sure datatype is acceptable
    if data_type not in VALID_DATA_TYPES:
        return {
            'success': False,
            'message': 'Data Type: %s not a valid data type' % (data_type),
        }

    #import ipdb; ipdb.set_trace()
    # start building new field
    new_field = Field(
        name = name,
        data_type = data_type,
        created_by_user_id = request.user.id,
        created_datetime = datetime.now(),
    )

    # if type is datetime make sure that a format is along with it

    if request.POST.get('data_type') == 'datetime':
        if not request.POST.get('datetime_format'):
            return {
                'success': False,
                'message': 'Missing a datetime format',
            }
        else:
            # add it
            new_field.datetime_format = request.POST['datetime_format']

    # save the new field
    #import ipdb; ipdb.set_trace()
    dataset.fields.append(new_field)
    dataset.save()
    return {'success': True}


@view_config(
    route_name='dataset_create', 
    permission='datasets', 
    request_method='POST', 
)
def create_dataset(request):
    """
    Create a new dataset schema.  
    Requires a unique collection name.
    """
    title = request.POST.get('title')
    if not title:
        raise Exception('title missing from request')

    # see if a dataset by this name already exists
    try:
        dataset = DatasetSchema.objects.get(title=title)
        raise Exception ('Title: %s has already been used' % 
                (title))
    except DatasetSchema.DoesNotExist:
        pass

    # create a datassetschema with this name and let the user add some
    # fields!
    new_dataset = DatasetSchema(
        created_by_user_id = request.user.id,
        created_datetime = datetime.now(),
        title = title,
    )
    # make sure to add slug 
    new_dataset.save()
    
    location = request.route_url('dataset_get', 
        slug=new_dataset.slug)
    return HTTPFound(location=location)


@view_config( 
    route_name='dataset_get', 
    permission='datasets', 
    request_method='GET', 
    renderer='ourdata:templates/create_dataset.mak'
)
def dataset_get(request):
    """Render the create_dataset template"""
    # make sure to get the title from here and load correctly

    # title should be valid and all form urls shoudl be appropriate
    return {}
