from ourdata.apps.common.utils import validate_email
from ourdata.apps.common.exceptions import ValidationError
from ourdata.apps.datasets.models import DatasetSchema
from ourdata.apps.users.models import User
import unittest
from pyramid import testing
from webtest import TestApp

class UtilsTests(unittest.TestCase): 
    """ Tests utils.py functions."""
    
    def test_email_validate(self):
        """
        Verify that an incorrect email can be detected,
        and a valid one can be detected.
        """

        #import ipdb; ipdb.set_trace()
        valid_email = 'test@test.com'
        invalid_email = 'testtest.com'

        validate_email(valid_email)
        try:
            validate_email(invalid_email)
            self.fail('invalid email not caught')
        except ValidationError:
            pass


class TestTemplate(unittest.TestCase):

    def setUp(self):
        from ourdata import main
        settings_dict = {'mongo_db_name': 'ourdata_test',
            'auth.salt': 'reallyrandom'}
        app = main({}, **settings_dict)
        self.testapp = TestApp(app)

        self.test_email = 'test@test.com'
        self.test_password = 'test'
        self.test_user = User.create_user(email=self.test_email,
                first_name='test', last_name='test', 
                password=self.test_password)


    def tearDown(self):
        testing.tearDown()
        # make sure to clear test_db every time
        # right now just delete the models that are used,  hacky
        User.objects.delete()
        DatasetSchema.objects.delete()


    def login(self, email, password):
        """
        Logs a user in.
        """
        post_params = {'email': email, 'password': password}
        response = self.testapp.post('/login', params=post_params, 
                                   status=302)

