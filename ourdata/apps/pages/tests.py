import os
import unittest
from urlparse import urlparse

from pyramid import testing
from webtest import TestApp

from ourdata.apps.common.tests import TestTemplate
from ourdata.apps.users.models import User


class PagesTests(TestTemplate):
    """Functional tests for all views.  If enough views split
    this up."""

    def test_home(self):
        result = self.testapp.get('/', status=200)

    def test_signup_get(self):
        result = self.testapp.get('/signup', status=200)

    def test_admin_dashboard_get(self):
        self._login(self.test_email, self.test_password)
        response = self.testapp.get('/dashboard', status=301)
        self.assertEqual(response.location, 'http://localhost/dashboard/admin')

    def test_user_dashboard_get(self):
        """
        Tests that a normal user account can load their 
        dashboard page with their API credentials.
        """
        new_user, new_user_password = self._create_test_user_through_signup_page()
        self._login(new_user.email, new_user_password)
        response = self.testapp.get('/dashboard', status=200)

    def test_login_required_dashboard_redirect(self):
        """
        Tests that if a user is not logged in, they are redirected to home page if
        they try to access the dashboard.
        """
        response = self.testapp.get('/dashboard', status=301)
        self.assertEqual(urlparse(response.location).path, '/')
        #import ipdb; ipdb.set_trace()

    def test_login_required_admin_dashboard_redirect(self):
        """
        Tests that if a user is not logged in, they are redirected to home page if
        they try to access the admin dashboard.
        """
        response = self.testapp.get('/dashboard/admin', status=301)
        self.assertEqual(urlparse(response.location).path, '/')
