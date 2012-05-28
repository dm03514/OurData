from mongoengine import *


class Field(EmbeddedDocument):
    """
    Contains meta data on a field name and field datatype as
    defined by a user.
    """
    name = StringField()
    data_type = StringField()
    datetime_format = StringField()
    created_by_user_id = ObjectIdField()
    created_datetime = DateTimeField()

    def __unicode__(self):
        return '%s %s' % (self.name, self.data_type)


class DatasetSchema(Document):
    """
    Contains the schema of a user defined collection.
    """
    created_by_user_id = ObjectIdField()
    created_datetime = DateTimeField()
    fields = ListField(EmbeddedDocumentField(Field))
    title = StringField()
    slug = StringField()

    def __unicode__(self):
        return self.title


VALID_DATA_TYPES = ['int', 'decimal', 'str', 'datetime']
