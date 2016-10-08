from tornado.testing import gen_test, AsyncTestCase

from bootcamp.lib.string import make_unicode


class TestString(AsyncTestCase):
    @gen_test
    def test_make_unicode(self):
        assert make_unicode('abc') == u'abc'
        assert make_unicode(u'abc') == u'abc'
