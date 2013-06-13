from pyramid.httpexceptions import HTTPMovedPermanently

def login_required(view_callable):
    """
    Make sure user is logged in, if not redirects them to the home page.
    """
    def inner(context, request):
        if request.user is None:
            return HTTPMovedPermanently(location=request.route_url('home'))

        return view_callable(context, request)

    return inner

