from pyramid.view import view_config

class ParamNotFoundError(Exception):
    """
    Raised when a required param is missing from 
    request.
    """
    pass


class APIBaseView(object):

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

    def __init__(self, request):
        """
        Make sure that store request for later use.
        """
        self.request = request

    @view_config(
        route_name='api_request', 
    )
    def api_request(self):
        # check required params

        # authenticate the request

        # call the corresponding request Type

        # get data/response/return value fromt he appropriate method
        # and make sure to render to user based on Accept header, either
        # application/json or as html
        # https://github.com/django/django/blob/master/django/views/generic/base.py
        return dispatch(self.request)

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Exception() 

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
        raise NotImplementedError() 
