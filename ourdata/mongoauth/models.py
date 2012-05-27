from datetime import datetime
from mongoengine import *
from ourdata.exceptions import UserExists
from ourdata.utils import encrypt_password, validate_email


class User(Document):
    email = StringField(required=True)
    first_name = StringField(required=True, max_length=50)
    #is_staff = BooleanField()
    #is_superuser = BooleanField()
    is_active = BooleanField()
    last_login = DateTimeField()
    last_name = StringField(required=True, max_length=50)
    password = StringField(required=True)
    datetime_joined = DateTimeField()
    groups = ListField(StringField())

    @classmethod
    def create_user(cls, email, first_name, last_name, password):
        """
        Responsible for validating new user input.  Hashes password
        and raises UserExists error if is duplicate. Creates and saves
        a new user.
        """
        # let validation error bubble up for right now
        validate_email(email)

        # check if user exists based on email
        try:
            cls.objects.get(email=email)
            # how should User be referred to ? cls or User?
            raise UserExists
        except User.DoesNotExist:
            pass

        # hash bpassword
        encrypted_password = encrypt_password(password)
        now_datetime = datetime.now()

        #import ipdb; ipdb.set_trace()

        new_user = cls(
            email = email, 
            first_name = first_name, 
            last_name = last_name, 
            password = encrypted_password,
            datetime_joined = now_datetime, 
            last_login = now_datetime,
            is_active = True
        )
        new_user.save()
        return new_user
