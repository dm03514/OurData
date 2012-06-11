from ourdata.apps.common.exceptions import ValidationError
from ourdata.apps.common.tests import TestTemplate
from ourdata.apps.users.models import APICredential, User
from ourdata.apps.users.utils import validate_email


class UsersTests(TestTemplate):

    def test_new_user_signup_post(self):
        post_params = {
            'first_name': 'Daniel',
            'last_name': 'Mican',
            'email': 'dm03514@gmail.com',
            'password': 'ourdata',
        }
        old_count = User.objects.all().count()
        response = self.testapp.post('/signup?test[]=test&test[]=test2', params=post_params, 
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
        self.assertNotEqual(None, authenticated_user)
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

    def test_api_credential_key_generation(self):
        """
        Verify we can generate two random unique keys for a user's
        access to a dataset.
        """
        self.login(self.test_email, self.test_password)
        self.create_and_populate_dataset()
        credential = APICredential()
        credential.generate_credential(
            user_id=self.test_user.id, 
            dataset_obj=self.dataset) 
        credential.save()
        self.assertNotEqual(credential.public_key, credential.private_key)
        for field in credential:
            self.assertTrue(getattr(credential, field))

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
