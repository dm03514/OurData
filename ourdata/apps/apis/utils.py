import hashlib
from json import JSONEncoder
import json
from mongoengine import connection
from operator import itemgetter
from bson import json_util


def is_valid_hmac_request(params_dict, private_key):
    """
    Check to see if a request is a valid hmac request
    @params multidict a multidict of params
    @return boolean
    """
    # make sure to copy the params_dict input, to avoid any side effects
    params_dict_copy = params_dict.copy()
    # remove the sig
    sig = params_dict_copy.pop('sig')
    return (generate_request_sig(params_dict_copy, private_key) == sig)


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
    cat_param_str = ''.join(['%s%s' % (x[0], x[1]) for x in sorted_list])
    # concat private_key
    cat_param_str += private_key
    # hash all everything together!
    h = hashlib.new('SHA1')
    h.update(cat_param_str)
    return h.hexdigest()

def generate_keys(user_id_str, dataset_name, salt):
    """
    Generate a set of keys for a specific dataset.
    Does this even work?
    """
    h = hashlib.new('SHA1')
    h.update(user_id_str)
    h.update(dataset_name)
    h.update(salt)
    public_key = h.hexdigest()
    h.update('private')
    private_key = h.hexdigest()
    return public_key, private_key


class QueryHelper():
    """
    Help abstract out the problem of querying over vastly
    different dataschemas.
    """

    def __init__(self, collection_name, params_dict, field_name=None):

        self.limit = 100
        self.sort_list = [('$natural', 1)]

        # get this collection
        db = connection.get_db()
        self.collection = db[collection_name]

        self.query_dict = self._build_query(params_dict, field_name)


    def _build_query(self, params_dict, field_name=None):
        """
        Populate query dict according to the request params.
        @param params_dict multidict of params for this query
        @return dict a mongo query ready to be executed by find
        """
        # add offset to `skip`
        query_dict = {}
        # if equalTo is present just use that to fetch result
        if 'equalTo' in params_dict:
           query_dict[field_name] = params_dict['equalTo'] 
        elif self._has_range(params_dict):
            if 'lessThan' in params_dict:
                query_dict[field_name] = {'$lt': params_dict['lessThan']}
            if 'greaterThan' in params_dict:
                query_dict[field_name] = {'$gt': params_dict['lessThan']}
            if 'lessThanEqualTo' in params_dict:
                query_dict[field_name] = {'$lte': params_dict['lessThan']}
            if 'greaterThanEqualTo' in params_dict:
                query_dict[field_name] = {'$gte': params_dict['lessThan']}
        return query_dict


    def get_results(self, serialized_as='json'):
        """
        Return a list of results serialized according to the
        given type'
        """
        # skip is implemented in find as kwarg
        results = self.collection.find(self.query_dict,
                                       limit=self.limit,
                                       sort=self.sort_list)

        return json.dumps([x for x in results], default=json_util.default)


    def _has_range(self, params_dict):
        """
        Check whethere this is a range query so a proper query
        dict can be built.
        @return boolean 
        """
        has_range = False
        range_params_list = ['lessThan', 'lessThanEqualTo',
            'greaterThan', 'greaterThanEqualTo']
        for range_param in range_params_list:
            if range_param in params_dict:
                has_range = True
        return has_range
