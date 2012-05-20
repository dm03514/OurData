from ourdata.mongoauth.models import User
import os
import unittest
from webtest import TestApp

from pyramid import testing
from mongoengine import *

class ViewFunctionalTests(unittest.TestCase):
    """Functional tests for all views.  If enough views split
    this up."""

    def setUp(self):
        from ourdata import main
        app = main({}, **{'mongo_db_name': 'ourdata_test'})
        self.testapp = TestApp(app)

    def tearDown(self):
        testing.tearDown()
        # make sure to clear test_db every time
        # right now just delete the models that are used,  hacky
        User.objects.delete()

    def test_home(self):
        result = self.testapp.get('/', status=200)

    def test_signup_get(self):
        result = self.testapp.get('/signup', status=200)

    def test_signup_post(self):
        post_params = {
            'first_name': 'Daniel',
            'last_name': 'Mican',
            'email': 'dm03514@gmail.com',
            'password': 'ourdata',
        }
        result = self.testapp.post('/signup', params=post_params, 
                                   status=302)
        #import ipdb; ipdb.set_trace()


class UtilsTests(unittest.TestCase): 
    """ Tests utils.py functions."""
    
    def test_email_validate(self):
        """
        Verify that an incorrect email can be detected,
        and a valid one can be detected.
        """
        from ourdata.utils import validate_email
        from ourdata.exceptions import ValidationError

        #import ipdb; ipdb.set_trace()
        valid_email = 'test@test.com'
        invalid_email = 'testtest.com'

        validate_email(valid_email)
        try:
            validate_email(invalid_email)
            self.fail('invalid email not caught')
        except ValidationError:
            pass
            
            
