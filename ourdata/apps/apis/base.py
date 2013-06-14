from pyramid.renderers import render_to_response
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

    def api_request(self):
        #import ipdb; ipdb.set_trace()
        # check required params

        # authenticate the request

        # call the corresponding request Type

        # get data/response/return value fromt he appropriate method
        # and make sure to render to user based on Accept header, either
        # application/json or as html
        # https://github.com/django/django/blob/master/django/views/generic/base.py
        data = self._dispatch(self.request)

        # encode data using the correct content type
        return self._render_response(data)

    @property
    def authenticator(self):
        """
        Abstract property which must contain a valid authenticator instance
        """
        raise NotImplementedError() 

    def check_request_params(self, required_params_list):
        """
        Make sure that a request is valid.
        raises a ParamNotFoundError with specifics
        """
        for param in required_params_list:
            if not self.request.GET.get(param):
                raise ParamNotFoundError('Missing %s from request' % (param))

    def _dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self._http_method_not_allowed)
        else:
            handler = self._http_method_not_allowed
        return handler(*args, **kwargs)

    #def has_required_params(self, required_params_list):

    def _http_method_not_allowed(self, *args, **kwargs):
        return Exception() 

    def _render_response(self, context_dict):
        """
        Returns a response with the correct headers/ content type, defaults to JSON.
        """
        return render_to_response('json', context_dict, self.request)
