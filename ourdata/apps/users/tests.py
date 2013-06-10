from ourdata.apps.apis.models import APICredential
from ourdata.apps.common.exceptions import ValidationError
from ourdata.apps.common.tests import TestTemplate
from ourdata.apps.users.models import User
from ourdata.apps.users.utils import validate_email


class UsersTests(TestTemplate):

    def test_new_user_signup_post(self):
        old_count = User.objects.all().count()

        self._create_test_user_through_signup_page()

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
        self._login(self.test_email, self.test_password)
        self._create_and_populate_dataset()
        credential = APICredential.generate_credential(
            user_id=self.test_user.id, 
            dataset_obj=self.dataset) 
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

    def test_edit_users_permissions_page_load_success(self):
        """
        Tests that admin can load page that allows them to grant permissions to a specific
        user.
        """
        new_user, new_user_password = self._create_test_user_through_signup_page()
        self._login(self.test_email, self.test_password)
        response = self.testapp.get('/user/permissions/edit/{}'.format(new_user.id), 
                                    status=200)
