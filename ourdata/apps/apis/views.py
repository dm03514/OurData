from pyramid.view import view_config

from ourdata.apps.apis.authentication import HMACAuthenticator
from ourdata.apps.apis.base import APIBaseView, ParamNotFoundError
from ourdata.apps.apis.models import APICredential
from ourdata.apps.apis.utils import is_valid_hmac_request, QueryHelper
from ourdata.apps.datasets.models import DatasetSchema


"""
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

    authenticator = HMACAuthenticator()

    @view_config(
        route_name='api_field_request', 
    )
    def api_field_request(self):
        return super(APIFieldRequest, self).api_request()
   
    def get(self):

        # all url values should be converted to the correct datatype
        query_params_list = ['lessThan', 'lessThanEqualTo',
            'greaterThan', 'greaterThanEqualTo', 'equalTo']
        for query_param in query_params_list:
            # check if the param is in params
            value_str = self.params_dict.get(query_param)
            if value_str:
                self.params_dict[query_param] = self.dataset.convert_field_value(
                    self.request.matchdict['field_name'], value_str,
                    from_timestamp=True)


        # all is good finally time to query!
        query_helper = QueryHelper(
            collection_name=self.dataset.title, 
            params_dict=self.params_dict,
            field_name=self.request.matchdict['field_name']
        )
        results = query_helper.get_results()
        return {'success': True, 'results': results}


class APIRequest(APIBaseView):

    authenticator = HMACAuthenticator()

    @view_config(
        route_name='api_request', 
    )
    def api_request(self):
        return super(APIRequest, self).api_request()

    def get(self):
        query_helper = QueryHelper(collection_name=self.dataset.title, 
                                   params_dict=self.params_dict)
        results = query_helper.get_results()
        #import ipdb; ipdb.set_trace()
        return {}
