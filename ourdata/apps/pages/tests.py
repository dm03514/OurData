from ourdata.apps.users.models import User
import os
import unittest
from webtest import TestApp

from pyramid import testing

class PagesTests(unittest.TestCase):
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

