from functools import reduce

"""
These functions let you handle python dicts like MongoDB docs
using a nested notation with dots: e.g. root.subdoc1.key1
"""

# from https://stackoverflow.com/a/46890853
def deep_get(dictionary, keys, default=None):
    """gets the value of a nested key"""
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

def deep_set(dictionary, keys, value):
    """Sets a value for a nested key"""
    keys = keys.split(".")
    last_key = keys.pop()
    sub_dict = dictionary
    for key in keys:
        sub_dict = sub_dict.get(key)
    sub_dict[last_key] = value

