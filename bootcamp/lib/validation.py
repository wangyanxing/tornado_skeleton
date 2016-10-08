from voluptuous import Invalid


def is_valid_uuid(uuid_value):
    """Test if the input is a valid uuid."""
    if not isinstance(uuid_value, basestring):
        return False
    import re
    return bool(
        re.compile(
            '^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$|'
            '^[a-f0-9]{8}[a-f0-9]{4}4[a-f0-9]{3}[89ab][a-f0-9]{3}[a-f0-9]{12}$'
        ).match(uuid_value)
    )


def is_valid_uuid_string(uuid_value):
    """Test if the input is a valid uuid string and return truthy/Exception."""
    if not isinstance(uuid_value, basestring):
        raise Invalid('validation_error.must_be_a_valid_string')

    if not is_valid_uuid(uuid_value):
        raise Invalid('validation_error.must_be_a_valid_uuid_v4')
    return uuid_value
