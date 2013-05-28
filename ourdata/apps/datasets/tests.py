from datetime import datetime
from ourdata.apps.common.tests import TestTemplate
from ourdata.apps.datasets.models import DatasetSchema, Field
import random


class DatasetsTests(TestTemplate):

    def test_dataset_get(self):
        """
        Verify the create dateset tepmlate can be loaded.
        self.login(self.test_email, self.test_password)
        self.testapp.get('/dataset/create', status=200)
        """
        pass
        # need to create a new dataset first before we can get it

    def test_dataset_create(self):
        """
        Verify that a new dataset can be created.
        """
        orig_count = DatasetSchema.objects.all().count()
        
        self.login(self.test_email, self.test_password)
        post_params_dict = {'title': 'new_dataset'}
        response = self.testapp.post('/dataset/create', 
                                    post_params_dict, status=302)

        sets_count = DatasetSchema.objects.all().count()
        self.assertEqual(sets_count, orig_count + 1)
        # should get the slug here vs the passed in title
        self.assertEqual(response.location, 'http://localhost/dataset/get/%s' % (post_params_dict['title']))

    def test_column_create(self):
        """
        Verify a data column can successfully be created.
        """
        self.login(self.test_email, self.test_password)

        # make sure to create a new dataset
        title = 'new_dataset'
        post_params_dict = {'title': title}
        response = self.testapp.post('/dataset/create', 
                                    post_params_dict, status=302)

        post_params_dict = {
            'name': 'new column',
            'data_type': 'datetime',     
            'datetime_format': 'YYYY-mm-dd',
        }
        response = self.testapp.post('/dataset/%s/column/create' % (title), 
                                     post_params_dict, 
                                     status=301)

        dataset = DatasetSchema.objects.get(title=title)
        self.assertEqual(len(dataset.fields), 1)


    def test_dataset_convert_field_value_int(self):
        """
        Tests that a datetime strings can succesffully converted to
        native python values.
        """
        dataset_schema = self.create_dataset_schema()
        new_field = Field(name='int_column',
                          data_type='int',
                          created_by_user_id=self.test_user.id,
                          created_datetime=datetime.now())
        dataset_schema.fields.append(new_field)
        dataset_schema.save()
        #import ipdb; ipdb.set_trace()
        for i in range(10): 
            rand_int = random.randint(1, 100000)
            converted_value = dataset_schema.convert_field_value('int_column', str(rand_int))
            self.assertEqual(converted_value, rand_int)
