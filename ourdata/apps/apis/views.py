from pyramid.view import view_config

from ourdata.apps.apis.authentication import HMACAuthenticationMixin
from ourdata.apps.apis.base import APIBaseView, ParamNotFoundError
from ourdata.apps.apis.models import APICredential
from ourdata.apps.apis.utils import is_valid_hmac_request, QueryHelper
from ourdata.apps.datasets.models import DatasetSchema
from ourdata.apps.users.models import User


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


class APIFieldRequest(APIBaseView):
    
    @view_config(
        route_name='api_field_get', 
        request_method='GET',
        renderer='json'
    )
    def api_field_get(self):

        try:    
            self.check_request_params(['sig', 'key'])
        except ParamNotFoundError as e:
            return {'success': False, 'message': e.message}

        # get the dataset for this title check that it contains
        try:
            dataset = DatasetSchema.objects.get(
                title=self.request.matchdict['dataset_slug'],
                fields__name=self.request.matchdict['field_name']
            )
        except DatasetSchema.DoesNotExist:
            return {
                'success': False,
                'message': 'No Dataset named: %s' % 
                    (self.request.matchdict['dataset_slug'])
            }

        params_dict = self.request.params.copy()

        # all url values should be converted to the correct datatype

        query_params_list = ['lessThan', 'lessThanEqualTo',
            'greaterThan', 'greaterThanEqualTo', 'equalTo']
        for query_param in query_params_list:
            # check if the param is in params
            value_str = params_dict.get(query_param)
            if value_str:
                params_dict[query_param] = dataset.convert_field_value(
                    self.request.matchdict['field_name'], value_str,
                    from_timestamp=True)

        # get credential associated with this request
        try:
            credential = APICredential.objects.get(
                public_key=self.request.GET['key'],
                dataset_id=dataset.id,
                is_active=True
            )
        except APICredential.DoesNotExist:
            return {
                'success': False,
                'message': 'Invalid Key',
            }

        # get user associated with this credential
        user = User.objects.get(id=credential.user_id, is_active=True)

        # check signature
        if not is_valid_hmac_request(params_dict, credential.private_key):
            return {
                'success': False,
                'message': 'Invalid Signature',
            }

        #import ipdb; ipdb.set_trace()
        # all is good finally time to query!
        query_helper = QueryHelper(
            collection_name=dataset.title, 
            field_name=self.request.matchdict['field_name'],
            params_dict=params_dict
        )
        results = query_helper.get_results()
        return {'success': True, 'results': results}


class APIRequest(HMACAuthenticationMixin, APIBaseView):

    def get(self):
        pass
