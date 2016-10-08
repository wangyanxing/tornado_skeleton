import re

_underscorer1 = re.compile(r'(.)([A-Z][a-z]+)')
_underscorer2 = re.compile('([a-z0-9])([A-Z])')


def camel_to_snake(string):
    subbed = _underscorer1.sub(r'\1_\2', string)
    return _underscorer2.sub(r'\1_\2', subbed).lower()


def snake_to_camel(string):
    components = string.split('_')
    return components[0] + "".join(x.title() for x in components[1:])
