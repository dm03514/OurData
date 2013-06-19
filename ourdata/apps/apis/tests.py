import json
import unittest
from urllib import urlencode

from ourdata.apps.apis.utils import generate_request_sig, is_valid_hmac_request
from ourdata.apps.common.tests import TestTemplate


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
        response = self.testapp.get('/api/%s/%s?%s' % 
            (self.dataset_title, 'int_column', urlencode(params_dict))
        )
        self.assertTrue(response.json['success'])
        results_list = json.loads(response.json['results'])
        self.assertGreater(len(results_list), 0)

    def test_generate_request_sig(self):
        self._login(self.test_email, self.test_password)
        self._create_and_populate_dataset()
        credential = self._generate_credentials(self.test_user, self.dataset)
        params_dict = {'key': credential.public_key}
        params_dict['sig'] = generate_request_sig(params_dict, credential.private_key)
        self.assertTrue(is_valid_hmac_request(params_dict, credential.private_key))

    def test_is_valid_hmac_request_params_dict_not_modified(self):
        """
        Makes sure that the first parameter (dict) of the function is not modefied.
        """
        params_dict = {'sig': '1231231234124', 'test1': 'test1', 'test2': 'test2'}
        params_dict_copy = params_dict.copy()
        is_valid_hmac_request(params_dict_copy, private_key='test')
        self.assertEqual(params_dict, params_dict_copy)

    def test_api_get_request_success(self):
        """
        Tests that a complete request can be returned from the api with all data in the api
        """
        self._login(self.test_email, self.test_password)
        self._create_and_populate_dataset()
        credential = self._generate_credentials(self.test_user, self.dataset)
        params_dict = {'key': credential.public_key}
        params_dict['sig'] = generate_request_sig(params_dict, credential.private_key)
        response = self.testapp.get('/api/{}?{}'.format(self.dataset.title, urlencode(params_dict)))
        expected_return_values = (
            {'key': 'results', 'type': list},
            {'key': 'count', 'type': int},
            {'key': 'next', 'type': str},
            {'key': 'previous', 'type': str}
        )
        for expected_values_dict in expected_return_values:
            self.assertTrue(expected_values_dict['key'] in response.json)
            self.assertIsInstance(response.json['results'], expected_values_dict['type'])
        #import ipdb; ipdb.set_trace()

    def test_api_get_request_dataset_not_found(self):
        """
        Tests that when a url with an incorrect dataset slug is requested a 404 
        error is raised.
        """
        self._login(self.test_email, self.test_password)
        self._create_and_populate_dataset()
        credential = self._generate_credentials(self.test_user, self.dataset)
        params_dict = {'key': credential.public_key}
        params_dict['sig'] = generate_request_sig(params_dict, credential.private_key)
        response = self.testapp.get('/api/datasetdoesnotexist?{}'.format(urlencode(params_dict)),
            status=404)

    def test_api_get_request_missing_params(self):
        """
        Tests that a request returns correct error when params are missing.
        """
        self._login(self.test_email, self.test_password)
        self._create_and_populate_dataset()
        credential = self._generate_credentials(self.test_user, self.dataset)
        params_dict = {'key': credential.public_key}
        response = self.testapp.get('/api/{}?{}'.format(self.dataset.title, 
                                                        urlencode(params_dict)),
                                                        status=400)

    def test_api_get_invalid_credential_not_found(self):
        """
        Tests that HTTPUnauthorized (401) is returned if an api credential is not found
        for the given key.
        """
        self._login(self.test_email, self.test_password)
        self._create_and_populate_dataset()
        credential = self._generate_credentials(self.test_user, self.dataset)
        params_dict = {'key': 'madddddeeeup'}
        params_dict['sig'] = generate_request_sig(params_dict, credential.private_key)
        response = self.testapp.get('/api/{}?{}'.format(self.dataset.title, 
                                                        urlencode(params_dict)),
                                                        status=401)
