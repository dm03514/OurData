from datetime import datetime
from mongoengine import *
from ourdata.apps.apis.utils import generate_keys

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

    @classmethod
    def generate_credential(cls, user_id, dataset_obj, salt='random'):
        # check if credential already exists
        try:
            cls.objects.get(dataset_id=dataset_obj.id,
                user_id=user_id)
            raise Exception('Credential Already Exists')
        except cls.DoesNotExist:
            pass
        new_credential = cls(
            is_active=True,
            approval_datetime=datetime.now(),
            dataset_id=dataset_obj.id,
            user_id=user_id,
        )
        new_credential.public_key, new_credential.private_key = generate_keys(str(user_id), dataset_obj.title, salt)
        new_credential.save()
        return new_credential
