from pyramid.view import view_config

@view_config(route_name='dataset_create', 
        permission='staff', 
        request_method='GET', 
        renderer='ourdata:templates/create_dataset.pt')
def create_dataset(request):
    """Render the create_dataset template"""
    return {}
