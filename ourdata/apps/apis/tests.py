import json
from ourdata.apps.apis.utils import generate_request_sig, is_valid_hmac_request
from ourdata.apps.common.tests import TestTemplate
from urllib import urlencode


class APIsTests(TestTemplate):

    def test_api_field_get(self):
        """
        Test that records can be pulled down using api_field_get.
        """
        #config.add_route('api_field_get', '/api/{dataset_title}/{field_name}/get')
        self._login(self.test_email, self.test_password)
        # create dataset and add some records to it
        self._create_and_populate_dataset()
        # add credentials to the test_user object
        credential = self._generate_credentials(self.test_user, self.dataset)
        params_dict = {'key': credential.public_key, 'lessThan': 10}
        params_dict['sig'] = generate_request_sig(params_dict, credential.private_key)
        response = self.testapp.get('/api/%s/%s/get?%s' % 
            (self.dataset_title, 'int_column', urlencode(params_dict))
        )
        #import ipdb; ipdb.set_trace()
        self.assertTrue(response.json['success'])
        results_list = json.loads(response.json['results'])
        self.assertGreater(len(results_list), 0)

    def test_generate_request_sig(self):
        # create dataset and add some records to it
        self._login(self.test_email, self.test_password)
        self._create_and_populate_dataset()
        credential = self._generate_credentials(self.test_user, self.dataset)
        params_dict = {'key': credential.public_key}
        params_dict['sig'] = generate_request_sig(params_dict, credential.private_key)
        self.assertTrue(is_valid_hmac_request(params_dict, credential.private_key))
