from datetime import datetime
from mongoengine import connection
from ourdata.apps.datasets.models import DatasetSchema
from ourdata.apps.users.models import User
from ourdata.apps.apis.models import APICredential
import unittest
from pyramid import testing
from webtest import TestApp


class TestTemplate(unittest.TestCase):

    def _create_dataset_schema(self):
        """
        Creates a test dataset schema.
        """
        dataset_schema = DatasetSchema(
            create_by_user_id=self.test_user.id,
            created_datetime=datetime.now(),
            title=u'test'
        )
        dataset_schema.save()
        return dataset_schema

    def _create_and_populate_dataset(self):
        """
        Create a test dataset and populate it with some random dattta
        """
        self.dataset_title = 'new_dataset'
        post_params_dict = {'title': self.dataset_title}
        response = self.testapp.post('/dataset/create', 
                                    post_params_dict, status=302)
        # attach this dataset to instance
        self.dataset = DatasetSchema.objects.get(title=self.dataset_title)
        post_params_dict = {
            'name': 'int_column',
            'data_type': 'int',     
        }
        url = str('/dataset/%s/column/create' % (self.dataset.slug))

        response = self.testapp.post(url, post_params_dict, status=301)
        collection = self.db[self.dataset_title]
        for i in range(120):
                collection.insert({'int_column': i})
        return self.dataset

    def _create_admin_user(self):
        """
        Create an admin user exposes it as self.test_user
        """
        self.test_email = 'test@test.com'
        self.test_password = 'test'
        self.test_user = User.create_user(email=self.test_email,
                first_name='test', last_name='test', 
                password=self.test_password, groups=['admin'])

    def _create_test_user_through_signup_page(self):
        """
        Creates a normal user with no permissions.  This is done by making a request to the
        signup page, not by creating the user directly through the User model.
        This returns a tuple the first item is the User object corresponding to this
        user, and the second is the user password.
        """
        post_params = {
            'first_name': 'Daniel',
            'last_name': 'Mican',
            'email': 'dm03514@gmail.com',
            'password': 'ourdata',
        }
        response = self.testapp.post('/signup?test[]=test&test[]=test2', params=post_params, 
                                   status=301)
        user_password = post_params['password']
        del post_params['password']
        return User.objects.get(**post_params), user_password

    def _drop_all_collections(self):
        """
        Loop through and delete all collections.
        """
        for collection_name in self.db.collection_names():
            if collection_name != 'system.indexes':
                self.db.drop_collection(collection_name)

    def _generate_credentials(self, user_obj, dataset_obj):
        """
        Generate and grant credentials to a specific user.
        """
        credential = APICredential.generate_credential(
            user_id=user_obj.id, 
            dataset_obj=self.dataset) 
        return credential

    def _login(self, email, password):
        """
        Logs a user in.
        """
        post_params = {'email': email, 'password': password}
        response = self.testapp.post('/login', params=post_params, 
                                   status=302)

    def setUp(self):
        from ourdata import main
        settings_dict = {'mongo_db_name': 'ourdata_test',
            'auth.salt': 'reallyrandom'}
        app = main({}, **settings_dict)
        self.testapp = TestApp(app)
        # get this db in pymongo interface for later
        self.db = connection.get_db()
        # clean up in case the last test errored
        self._drop_all_collections()
        # create an admin
        self._create_admin_user()

    def tearDown(self):
        testing.tearDown()
        # make sure to clear test_db every time
        # right now just delete the models that are used,  hacky
        self._drop_all_collections()


class CommonTests(TestTemplate):

    def test_slugify(self):
        """
        Test that the slugify utiltity works.
        """
        from ourdata.apps.common.utils import slugify
        title = u'This should be slugif":ed yall/'
        self.assertEqual(slugify(title), u'this-should-be-slugifed-yall')
