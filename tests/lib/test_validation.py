from tornado.testing import gen_test, AsyncTestCase
from voluptuous import Invalid

from bootcamp.lib.validation import is_valid_uuid_string, is_valid_uuid


class TestValidation(AsyncTestCase):
    valid_uuid = '2bd3c6b4-ce9b-4155-b258-3dd8152f431e'

    @gen_test
    def test_is_valid_uuid(self):
        assert is_valid_uuid(self.valid_uuid) is True
        assert is_valid_uuid('not a valid uuid') is False
        assert is_valid_uuid(None) is False

    @gen_test
    def test_is_valid_uuid_string(self):
        assert is_valid_uuid_string(self.valid_uuid) == self.valid_uuid

        try:
            is_valid_uuid_string('not a valid uuid')
        except Invalid:
            pass
        else:
            raise AssertionError('Expected test to raise Invalid.')

        try:
            is_valid_uuid_string([])
        except Invalid:
            pass
        else:
            raise AssertionError('Expected test to raise Invalid.')
