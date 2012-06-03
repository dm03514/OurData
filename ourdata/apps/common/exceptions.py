class FieldNotFoundError(Exception):
    """Error if a field definition is not found in a dataset schema."""
    pass

class DataConversionError(Exception):
    """Error while performing type conversion"""
    pass

class ValidationError(Exception):
    """Something is generally not valid"""
    pass

class UserExists(Exception):
    """Something is generally not valid"""
    pass

