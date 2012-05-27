from ourdata.mongoauth.models import User

from pyramid.security import unauthenticated_userid

def get_user(request):
    """
    Get a user object based on the userid present in the cookie.  
    """
    user_id = unauthenticated_userid(request)
    if user_id is not None:
        try:
            User.objects.get(id=user_id)
        except User.DoesNotExist:
            pass
        
