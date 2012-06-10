from ourdata.apps.apis.base import AuthAPIRequestView, ParamNotFoundError
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
    - less_than = value
    - greater_than = value
    - equal = value



decimal/integer/datetime fields should be able to have either >value <value or range
http://api.mongodb.org/python/2.0/tutorial.html#range-queries


string should be able to do == and contains
"""




class APIAuthFieldGetRequest(AuthAPIRequestView):
    
    @view_config(
        route_name='api_field_get', 
        request_method='GET',
        renderer='json'
    )
    def api_get(self):

        #import ipdb; ipdb.set_trace()
        try:    
            self.check_request_params(['sig', 'key'])
        except ParamNotFoundError as e:
            return {'success': False, 'message': e.message}

        # get user associated with this key
        try:
            user = User.objects.get(id=self.request.GET['key'])
        except User.DoesNotExist:
            return {
                'success': False,
                'message': 'No User exists for this key',
            }


        # check signature
        #if not is_authenticated_request(request.params.copy(), user.
        return {}
