from ourdata.apps.common.utils import validate_email
from ourdata.apps.common.exceptions import ValidationError
import unittest

class UtilsTests(unittest.TestCase): 
    """ Tests utils.py functions."""
    
    def test_email_validate(self):
        """
        Verify that an incorrect email can be detected,
        and a valid one can be detected.
        """

        #import ipdb; ipdb.set_trace()
        valid_email = 'test@test.com'
        invalid_email = 'testtest.com'

        validate_email(valid_email)
        try:
            validate_email(invalid_email)
            self.fail('invalid email not caught')
        except ValidationError:
            pass
