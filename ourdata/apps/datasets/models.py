from datetime import datetime
from ourdata.apps.common.exceptions import DataConversionError, FieldNotFoundError
from mongoengine import *


class Field(EmbeddedDocument):
    """
    Contains meta data on a field name and field datatype as
    defined by a user.
    """
    name = StringField(required=True)
    data_type = StringField(required=True)
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

    def convert_field_value(self, field_name, field_value_str, 
                                            from_timestamp=False):
        """
        Convert a given field_name's value to it's internal datatype.
        Raises a DataConversion error if there is an issue.
        Might have to create a dictionary of fields to datatypes
        Should this even be here???
        """
        # look for a field with this field_name
        field_declaration = None
        for field in self.fields:
            if field.name == field_name:
                field_declaration = field
                break
        if field_declaration is None:
            raise FieldNotFoundError 

        # if data type is string we can just return value now
        if field_declaration.data_type == 'str':
            return field_value_str

        # try converting the string value to a python datatype
        conversion_f = VALID_DATA_TYPES[field_declaration.data_type]['function']
        try:
            # check if this is a datateme becasues then we need
            # to pass the datetime formatting str
            if field_declaration.data_type == 'datetime' and not from_timestamp:
                return conversion_f(field_value_str, 
                                    field_declaration.datetime_format)
            elif field_declaration.data_type == 'datetime' and from_timestamp:
                # convert from timestamp
                return datetime.fromtimestamp(field_value_str)

            # else just return the normal function
            return conversion_f(field_value_str)
        except ValueError:
            raise DataConversionError



VALID_DATA_TYPES = {
    'int': {
        'function': int,
    },
    'decimal': {
        'function': float,
    }, 
    'str': {}, 
    'datetime': { 
        'function': datetime.strptime,
    }
}
