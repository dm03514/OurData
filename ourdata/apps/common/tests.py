from mongoengine import connection
from ourdata.apps.datasets.models import DatasetSchema
from ourdata.apps.users.models import User, APICredential
import unittest
from pyramid import testing
from webtest import TestApp


class TestTemplate(unittest.TestCase):

    def create_and_populate_dataset(self):
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
        response = self.testapp.post('/dataset/%s/column/create' % (self.dataset_title), 
                post_params_dict, status=200)
        collection = self.db[self.dataset_title]
        for i in range(20):
                collection.insert({'new_column': i})

    def create_admin_user(self):
        """
        Create an admin user exposes it as self.test_user
        """
        self.test_email = 'test@test.com'
        self.test_password = 'test'
        self.test_user = User.create_user(email=self.test_email,
                first_name='test', last_name='test', 
                password=self.test_password, groups=['admin'])

    def drop_all_connections(self):
        """
        Loop through and delete all collections.
        """
        for collection_name in self.db.collection_names():
            if collection_name != 'system.indexes':
                self.db.drop_collection(collection_name)

    def generate_credentials(self, user_obj, dataset_obj):
        """
        Generate and grant credentials to a specific user.
        """
        credential = APICredential()
        credential.generate_credential(
            user_id=user_obj.id, 
            dataset_obj=self.dataset) 
        return credential.save()

    def login(self, email, password):
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
        self.drop_all_connections()
        # create an admin
        self.create_admin_user()

    def tearDown(self):
        testing.tearDown()
        # make sure to clear test_db every time
        # right now just delete the models that are used,  hacky
        #import ipdb; ipdb.set_trace()
        self.drop_all_connections()
