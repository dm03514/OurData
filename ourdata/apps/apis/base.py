

class ParamNotFoundError(Exception):
    """
    Raised when a required param is missing from 
    request.
    """
    pass


class APIBaseView(object):


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


    def is_authenticated(self):
        """
        Abstract method which checks if a request is authenticated.
        @return boolean 
        """
        raise Exception('Not Implemented')
