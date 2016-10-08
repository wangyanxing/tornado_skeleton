def make_unicode(string_or_other):
    if isinstance(string_or_other, str):
        return unicode(string_or_other, 'utf8')
    return string_or_other
