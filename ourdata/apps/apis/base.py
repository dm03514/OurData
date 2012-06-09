

class ParamNotFoundError(Exception):
    """
    Raised when a required param is missing from 
    request.
    """
    pass


class AuthAPIRequestView(object):


    def __init__(self, request):
        """
        Make sure that store request for later use.
        """
        self.request = request


    def check_request_params(self, required_params_list):
        """
        Make sure that a request is valid.
        raises a ParamNotFoundError with specifics
        """
        for param in required_params_list:
            if not self.request.GET.get(param):
                raise ParamNotFoundError('Missing %s from request' % (param))


    def is_valid_sig(self):
        """
        Check that a signature for a request is valid.
        @return boolean 
        """
        pass
