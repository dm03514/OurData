from ourdata.apps.apis.utils import is_valid_hmac_request

class InvalidCredentialsError(Exception):
    """
    Raised when a required param is missing from 
    request.
    """
    pass

class HMACAuthenticator(object):
    
    def is_authenticated(self, request_params_dict, private_key):
        """
        Makes sure that request is valid.
        """
        if not is_valid_hmac_request(request_params_dict, private_key):
            raise InvalidCredentialsError()
