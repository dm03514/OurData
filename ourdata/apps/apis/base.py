from pyramid.httpexceptions import HTTPNotFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config

from ourdata.apps.apis.authentication import InvalidCredentialsError 
from ourdata.apps.apis.models import APICredential
from ourdata.apps.datasets.models import DatasetSchema

"""
# authentication

    1) all params should be split up into a dictionary and ordered by key
    2) append all those params together as a string and 
        concat the privatekey
    3) sha1 that string
    4) attach that as value of 'sig' param to the request
"""

class ParamNotFoundError(Exception):
    """
    Raised when a required param is missing from 
    request.
    """
    pass


class APIBaseView(object):

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    required_params_list = ['sig', 'key'] 

    def __init__(self, request):
        """
        Make sure that store request for later use.
        """
        self.request = request

    def api_request(self):
        """
        Validates and authenticates the api request.  Will call the appropriate request
        method of the child class, ie `get`, `post`, and redner that data appropriatly
        """
        # check that this dataset is valid,
        # dataset is identified by the slug portion of the url
        try:
            self.dataset = DatasetSchema.objects.get(
                title=self.request.matchdict['dataset_slug']
            )
        except DatasetSchema.DoesNotExist as e:
            return self._render_response(http_exception=HTTPNotFound)

        # check all required params are present
        try:
            self.has_required_params()
        except ParamNotFoundError as e:
            raise e

        # get the credential of the user making the request
        try:
            self.credential = APICredential.objects.get(
                public_key=self.request.params['key'],
                dataset_id=self.dataset.id,
                is_active=True
            )
        except APICredential.DoesNotExist as e:
            raise e

        # authenticate the request
        try:
            self.authenticator.is_authenticated(self.request.params, 
                                                self.credential.private_key)
        except InvalidCredentialsError as e:
            raise e

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

    def _dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self._http_method_not_allowed)
        else:
            handler = self._http_method_not_allowed
        return handler(*args, **kwargs)

    def _get_api_credential(self):
        """
        Gets the credential associated with the request.key value or raises
        APICredential.DoesNotExist error.
        """

    def has_required_params(self):
        """
        Checks that all params in `required_params_list` are present in the request.
        Raises a ParamNotFound error if one is missing.
        """
        for expected_param in self.required_params_list:
            if not self.request.params.get(expected_param):
                raise ParamNotFoundError('Missing %s from request' % (expected_param))
          
    def _http_method_not_allowed(self, *args, **kwargs):
        return Exception() 

    def _render_response(self, context_dict={}, http_exception=None):
        """
        Returns a response with the correct headers/ content type, defaults to JSON.
        If there is an http_exception present, the response will contain information
        from that exception.  The exceptions are all the pyramid builtins 
        pyramid.httpexceptions
        http://pyramid.readthedocs.org/en/1.0-branch/api/httpexceptions.html#subclass-usage-notes
        """
        response = render_to_response('json', context_dict, self.request)
        #import ipdb; ipdb.set_trace()
        if http_exception is not None:
            response.status_int = http_exception.code
        return response
