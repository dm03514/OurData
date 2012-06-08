

"""
# authentication

    1) all params should be split up into a dictionary and ordered by key
    2) append all those params together as a string and 
        concat the privatekey
    3) sha1 that string
    4) attach that as value of 'sig' param to the request

# querying
    - list of fields comma seperated? is that legal?
    - dates should be unix timestamps


decimal/integer/datetime fields should be able to have either >value <value or range
http://api.mongodb.org/python/2.0/tutorial.html#range-queries


string should be able to do == and contains
"""


