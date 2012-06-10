from ourdata.apps.apis.utils import generate_request_sig, is_authenticated_request
from ourdata.apps.common.tests import TestTemplate


class APIsTests(TestTemplate):

    def test_api_field_get(self):
        """
        Test that records can be pulled down using api_field_get.
        """
        #config.add_route('api_field_get', '/api/{dataset_title}/{field_name}/get')
        self.login(self.test_email, self.test_password)
        # create dataset and add some records to it
        self.create_and_populate_dataset()
        # add credentials to the test_user object
        self.generate_credentials(self.test_user, self.dataset_title)

        response = self.testapp.get('/api/%s/%s/get' % (self.dataset_title, 'int_column'))
        self.assertTrue(response.json['success'])

    def test_generate_request_sig(self):
        # create dataset and add some records to it
        self.login(self.test_email, self.test_password)
        self.create_and_populate_dataset()
        self.generate_credentials(self.test_user, self.dataset_title)
        public_key = self.test_user.api_credentials[0].public_key
        private_key = self.test_user.api_credentials[0].private_key
        params_dict = {'key': public_key}
        params_dict['sig'] = generate_request_sig(params_dict, private_key)
        self.assertTrue(is_authenticated_request(params_dict, private_key))
