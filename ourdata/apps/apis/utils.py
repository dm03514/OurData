from mongoengine import connection
import hashlib
from operator import itemgetter


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
    cat_param_str = ''.join('%s%s' % (x[0], x[1]) for x in sorted_list)
    # concat private_key
    cat_param_str += private_key
    # hash all everything together!
    h = hashlib.new('SHA1')
    h.update(cat_param_str)
    return h.hexdigest()


def query_results(collection_name, field_name, params_dict):
    """
    Query a collection based on a set of user params.
    """
    import ipdb; ipdb.set_trace()
    db = connection.get_db()
    collection = db[collection_name]
    query_dict = {}
    if 'equal_to' in params_dict:
       query_dict[field_name] = params_dict['equal_to'] 
    else:
        # check to see if this is a range query
        # there has to be an eloquent way to do this.
        # make sure that all values are of the correct type not str
        if 'less_than' in params_dict:
            query_dict[field_name] = {'$lt': params_dict['less_than']}
        if 'greater_than' in params_dict:
            query_dict[field_name] = {'$gt': params_dict['less_than']}
    results = collection.find(query_dict)
