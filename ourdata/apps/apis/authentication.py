from ourdata.apps.apis.utils import is_valid_hmac_request


class HMACAuthenticator(object):
    
    def is_authenticated(self, request_params_dict, private_key):
        """
        Makes sure that request is valid.
        """
        return is_valid_hmac_request(request_params_dict, private_key)
