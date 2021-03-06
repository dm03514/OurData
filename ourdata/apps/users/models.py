from datetime import datetime
from mongoengine import *
from ourdata.apps.common.exceptions import UserExists
from ourdata.apps.users.utils import encrypt_password, validate_email


class User(Document):
    email = StringField(required=True)
    first_name = StringField(required=True, max_length=50)
    is_active = BooleanField()
    last_login = DateTimeField()
    last_name = StringField(required=True, max_length=50)
    password = StringField(required=True)
    datetime_joined = DateTimeField()
    groups = ListField(StringField())
    permissions = ListField(StringField())

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def has_permission(self, permission):
        """
        Test to see if a user has a specific permission.
        @param permission str the permission name
        @return boolean
        """
        if permission in self.permissions:
            return True
        return False

    @property
    def id_as_str(self):
        """
        Returns the id as a string.
        """
        return str(self.id)

    def is_member_of(self, group):
        """
        Check if user is member of a group.
        """
        if group in self.groups:
            return True
        return False

    @property
    def is_admin(self):
        return self.is_member_of('admin') 

    @classmethod
    def authenticate(cls, email, password):
        """
        Check to see if a user's credentials are correct.

        @param email string
        @param password string
        @return User object or None
        """
        encrypted_password = encrypt_password(password)
        try:
            user = cls.objects.get(email=email, 
                            password=encrypted_password, is_active=True)
            return user
        except cls.DoesNotExist:
            return None

    @classmethod
    def create_user(cls, email, first_name, last_name, password,
                        groups=[]):
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

        new_user = cls(
            email = email, 
            first_name = first_name, 
            last_name = last_name, 
            password = encrypted_password,
            datetime_joined = now_datetime, 
            last_login = now_datetime,
            is_active = True
        )
        if groups:
            new_user.groups = groups
        new_user.save()
        return new_user
