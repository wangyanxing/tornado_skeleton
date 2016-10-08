import re

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')


def coerce_camelcase_to_snakecase(string):
    """Stolen from stack overflow"""
    subbed = _underscorer1.sub(r'\1_\2', string)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def coerce_snakecase_to_camelcase(string):
    """Gracefully borrowed from stack overflow."""
    components = string.split('_')
    return components[0] + "".join(x.title() for x in components[1:])


def coerce_dict_keys(dictionary, to_camel_case=False, to_snake_case=False):
    """Helper function to coerce a dictionary's keys."""
    assert to_camel_case != to_snake_case
    coerce_func = (coerce_camelcase_to_snakecase if to_snake_case
                   else coerce_snakecase_to_camelcase)
    return {coerce_func(key): dictionary[key] for key in dictionary}
