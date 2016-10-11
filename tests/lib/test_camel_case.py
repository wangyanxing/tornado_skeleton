from bootcamp.lib.camel_case import camel_to_snake, snake_to_camel
from tornado.testing import AsyncTestCase, gen_test


class TestCamelCase(AsyncTestCase):
    @gen_test
    def test_camel_to_snake(self):
        assert camel_to_snake('abcAbc') == 'abc_abc'

    @gen_test
    def test_snake_to_camel(self):
        assert snake_to_camel('abc_abc') == 'abcAbc'
