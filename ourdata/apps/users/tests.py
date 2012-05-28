from ourdata.apps.common.tests import TestTemplate
from ourdata.apps.users.models import User


class UsersTests(TestTemplate):

    def test_new_user_signup_post(self):
        post_params = {
            'first_name': 'Daniel',
            'last_name': 'Mican',
            'email': 'dm03514@gmail.com',
            'password': 'ourdata',
        }
        old_count = User.objects.all().count()
        response = self.testapp.post('/signup', params=post_params, 
                                   status=302)
        # make sure a user has been created.
        new_count = User.objects.all().count()
        self.assertEqual(new_count, old_count + 1)

    def test_authenticate(self):
        """
        Verify that User autheticate method can match credentials
        and return a user if it should.
        """
        authenticated_user = User.authenticate(self.test_user.email, 
                                            self.test_password) 
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(self.test_user.id, authenticated_user.id)

    def test_login(self):
        """
        Verify the login method can successfully detect and login
        a user.
        """
        post_params = {'email': self.test_email, 
            'password': self.test_password}
        response = self.testapp.post('/login', params=post_params, 
                                   status=302)
        self.assertEqual(response.location, 'http://localhost/dashboard')
        #import ipdb; ipdb.set_trace()

    def test_logout(self):
        """
        Verify a user can logout.
        """
        post_params = {'email': self.test_email, 
            'password': self.test_password}
        response = self.testapp.post('/login', params=post_params, 
                                   status=302)
        self.assertEqual(response.location, 'http://localhost/dashboard')
        response = self.testapp.get('/logout', status=302)
        self.assertEqual(response.location, 'http://localhost/')
