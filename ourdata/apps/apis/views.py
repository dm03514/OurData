from ourdata.apps.apis.base import AuthAPIRequestView, ParamNotFoundError
from ourdata.apps.apis.utils import is_authenticated_request
from ourdata.apps.datasets.models import DatasetSchema
from ourdata.apps.users.models import User
from ourdata.apps.apis.models import APICredential
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

        try:    
            self.check_request_params(['sig', 'key'])
        except ParamNotFoundError as e:
            return {'success': False, 'message': e.message}

        #import ipdb; ipdb.set_trace()
        # get the dataset for this title check that it contains
        try:
            dataset = DatasetSchema.objects.get(
                title=self.request.matchdict['dataset_title'],
                fields__name=self.request.matchdict['field_name']
            )
        except DatasetSchema.DoesNotExist:
            return {
                'success': False,
                'message': 'No Dataset named: %s' % 
                    (self.request.matchdict['dataset_title'])
            }

        # get credential associated with this request
        try:
            credential = APICredential.objects.get(
                public_key=self.request.GET['key']
            )
        except APICredential.DoesNotExist:
            return {
                'success': False,
                'message': 'No User exists for this key',
            }

        # get user associated with this credential
        user = User.objects.get(id=credential.user_id)

        # check signature
        if not is_authenticated_request(self.request.params.copy(), 
                                                credential.private_key):
            return {
                'success': False,
                'message': 'Invalid Signature',
            }
             
        return {'success': True}
