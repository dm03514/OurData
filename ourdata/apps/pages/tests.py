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

