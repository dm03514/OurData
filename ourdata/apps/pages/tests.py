from ourdata.apps.common.tests import TestTemplate
from ourdata.apps.users.models import User
import os
import unittest
from webtest import TestApp

from pyramid import testing

class PagesTests(TestTemplate):
    """Functional tests for all views.  If enough views split
    this up."""

    def test_home(self):
        result = self.testapp.get('/', status=200)

    def test_signup_get(self):
        result = self.testapp.get('/signup', status=200)

    def test_admin_dashboard_get(self):
        self._login(self.test_email, self.test_password)
        response = self.testapp.get('/dashboard', status=302)
        self.assertEqual(response.location, 'http://localhost/dashboard/admin')
        #import ipdb; ipdb.set_trace()

    def test_user_dashboard_get(self):
        """
        Tests that a normal user account can load their dashboard page with their API credentials.
        """
        self.fail()
