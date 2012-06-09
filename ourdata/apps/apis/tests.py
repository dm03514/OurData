from ourdata.apps.common.tests import TestTemplate


class APIsTests(TestTemplate):

    def test_api_field_get(self):
        """
        Test that records can be pulled down using api_field_get.
        """
        #config.add_route('api_field_get', '/api/{dataset_title}/{field_name}/get')
        # create dataset and add some records to it
        self.login(self.test_email, self.test_password)
        self.create_and_populate_dataset()
        import ipdb; ipdb.set_trace()
