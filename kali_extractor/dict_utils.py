from functools import reduce
import re

"""
    This module eases handling the dictionaries parsed from the XML files.
    They give you a xpath-like (very partial) interface to get and set
    nested keys using a slashed notation like root/subdocs[2]/key1
    The main usecase is to normalize fields so that they are always arrays.
"""

XPATH_PART = r"(.*)\[(\d+)\]"

def xpath_to_keys(selector):
    """
        Splits a selector down to individual field names and indexes
        e.g. xpath_to_keys('root/subdocs[2]/key1') => ['root', 'subdocs', 2, 'key1']
    """
    parts = [p for p in selector.split("/") if p != '']
    keys = []
    for part in parts:
        match_data = re.match(XPATH_PART, part)
        if match_data:
            name, idx = match_data.groups()
            keys += [name, int(idx)]
        else:
            keys += [part]
    return keys

def deep_set(dictionary, xpath_selector, value):
    """
        Sets a value for a nested key.
        e.g. deep_set({'a': [{'b': 10}, {'b': 20}]}, 'a[1]/b', 30) will set the b value in the second item
    """
    keys = xpath_to_keys(xpath_selector)
    last_key = keys.pop()
    sub_dict = dictionary
    for key in keys:
        sub_dict = sub_dict[key]
    sub_dict[last_key] = value

def deep_get(dictionary, xpath_selector):
    """
        yields nested values from a dictionary with the associated selecting keys.
        e.g. deep_get({'a': {'b': 10}}, 'a/b']) returns (10, 'a/b'])
        e.g. deep_get({'a': [{'b': 10}, {'b': 20}]}, 'a/b') yields (10, 'a[0]/b') and then (20, 'a[1]/b'])
    """
    keys = xpath_to_keys(xpath_selector)
    yield from recursive_get(dictionary, keys)

def recursive_get(current_dict, keys, built_selector=''):
    if current_dict is not None:
        key = keys[0]
        leftover_keys = keys[1:]
        value = current_dict.get(key)
        if len(leftover_keys) == 0:
            if key in current_dict.keys():
                yield value, "%s/%s" % (built_selector, key)
        elif isinstance(value, list):
            for idx, child in enumerate(value):
                yield from recursive_get(child, leftover_keys, "%s/%s[%s]" % (built_selector, key, idx))
        else:
            yield from recursive_get(value, leftover_keys, "%s/%s" % (built_selector, key))



