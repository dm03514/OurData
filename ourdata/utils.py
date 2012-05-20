import hashlib
from ourdata.exceptions import ValidationError
import re

def validate_email(email_address):
    """
    Validate an email or raise a ValidateException
    Only testing against email regex right now to get going
    from:
    https://github.com/django/django/blob/master/django/core/validators.py
    """
    email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$)'  # domain
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE) 

    if not email_re.search(email_address):
        raise ValidationError('%s not valid email address' % 
                              (email_address))

def encrypt_password(raw_password):
    """
    Encrypt a password using the suggested hashing algorithm.
    """
    h = hashlib.new('SHA256')
    h.update(raw_password)
    return h.hexdigest()
