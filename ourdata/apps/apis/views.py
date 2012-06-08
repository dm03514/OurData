from pyramid.view import view_config


"""
# authentication

    1) all params should be split up into a dictionary and ordered by key
    2) append all those params together as a string and 
        concat the privatekey
    3) sha1 that string
    4) attach that as value of 'sig' param to the request

# querying
    - list of fields comma seperated? is that legal?
    - dates should be unix timestamps


decimal/integer/datetime fields should be able to have either >value <value or range
http://api.mongodb.org/python/2.0/tutorial.html#range-queries


string should be able to do == and contains
"""


@view_config(route_name='api_field_get', request_method='GET',
             renderer='json')
def api_get(request):
    """
    Return results from a dataset based on a one field query.
    Must include dataset title, field name and various GET params
    This auth might be better as a cbv? 
    http://ruslanspivak.com/2012/03/02/class-based-views-in-pyramid/
    """
    #validate request
    required_params_list = ['sig', 'key']
    for param in required_params_list:
        if not request.GET.get(param):
            return {
                'success': False,
                'message': 'Missing %s from request' % (param),
            }

    # get user associated with this 
    try:
        user = User.objects.get(id=request.GET['key'])
    except User.DoesNotExist:
        return {
            'success': False,
            'message': 'No User exists for this key',
        }

    
    return {}
