from datetime import datetime
import hashlib
from mongoengine import *

class APICredential(Document):
    """
    Contains credentials for a specific api.
    """
    public_key = StringField(required=True)
    private_key = StringField(required=True)
    is_active = BooleanField(required=True)
    approval_datetime = DateTimeField()
    dataset_id = ObjectIdField()
    user_id = ObjectIdField()

    def generate_credential(self, user_id, dataset_obj, salt='random'):
        self.is_active = True
        self.approval_datetime = datetime.now()
        self.dataset_id = dataset_obj.id
        self.user_id = user_id
        self._generate_keys(str(user_id), dataset_obj.title, salt)

    def _generate_keys(self, user_id_str, dataset_name, salt):
        """
        Generate a set of keys for a specific dataset.
        Does this even work?
        """
        h = hashlib.new('SHA1')
        h.update(user_id_str)
        h.update(dataset_name)
        h.update(salt)
        self.public_key = h.hexdigest()
        h.update('private')
        self.private_key = h.hexdigest()
