from bootcamp.lib.string import make_unicode
from tornado.testing import AsyncTestCase, gen_test


class TestString(AsyncTestCase):
    @gen_test
    def test_make_unicode(self):
        assert make_unicode('abc') == u'abc'
        assert make_unicode(u'abc') == u'abc'
