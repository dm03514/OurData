import hashlib
from operator import itemgetter
from urllib import urlencode


def is_authenticated_request(params, private_key):
    """
    Check to see if a request is authenticated or not.
    @params multidict a multidict of params
    @return boolean
    """
    # remove the sig
    sig = params.pop('sig')
    return (generate_request_sig(params, private_key) == sig)


def generate_request_sig(params_dict, private_key):
    """
    Caluculate a signature for a set of request params.
    @param params_dict a dictionary of values that will be included
    they query
    @param private_key str the private key for this user
    @return str the signature
    """
    # sort params_dict by key
    sorted_list = sorted(params_dict.items(), key=itemgetter(0))
    # combine all values into a string
    cat_param_str = ''.join(x[0]+x[1] for x in sorted_list)
    # concat private_key
    cat_param_str += private_key
    # hash all everything together!
    h = hashlib.new('SHA1')
    h.update(cat_param_str)
    return h.hexdigest()
