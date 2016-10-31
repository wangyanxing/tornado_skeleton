import binascii


from bootcamp.handlers.base import BaseHandler
from bootcamp.services.datastores.user_store import UserStore
import jwt
import mock

from tornado import gen
from tornado.test.web_test import WebTestCase


class CookieTest(WebTestCase):
    def get_app_kwargs(self):
        return {'cookie_secret': 'test_secret'}

    def get_handlers(self):
        class SetCookieHandler(BaseHandler):
            def get(self):
                self.set_cookie('str', 'asdf')
                self.set_cookie('unicode', u'qwer')
                self.set_cookie('bytes', b'zxcv')

        class GetCookieHandler(BaseHandler):
            def get(self):
                self.write(self.get_cookie('foo', 'default'))

        class XSRFHandler(BaseHandler):
            def get(self):
                self.write(self.xsrf_token)

        class SetUserCookieHandler(BaseHandler):
            def get(self):
                self.set_user_cookie({'a': 'b'})

        class GetUserCookieHandler(BaseHandler):
            def get(self):
                self.write(str(self.get_user_cookie()))

        return [
            ('/set', SetCookieHandler),
            ('/get', GetCookieHandler),
            ('/xsrf', XSRFHandler),
            ('/set_user_cookie', SetUserCookieHandler),
            ('/get_user_cookie', GetUserCookieHandler),
        ]

    def test_set_cookie(self):
        response = self.fetch('/set')
        self.assertEqual(sorted(response.headers.get_list('Set-Cookie')),
                         ['bytes=zxcv; httponly; Path=/; secure',
                          'str=asdf; httponly; Path=/; secure',
                          'unicode=qwer; httponly; Path=/; secure'])

    def test_get_cookie(self):
        response = self.fetch('/get', headers={'Cookie': 'foo=bar'})
        self.assertEqual(response.body, b'bar')

        response = self.fetch('/get', headers={'Cookie': 'foo="bar"'})
        self.assertEqual(response.body, b'bar')

    @mock.patch.object(binascii, 'b2a_hex')
    def test_xsrf_token(self, mock_hex):
        mock_hex.return_value = 'foo'
        response = self.fetch('/xsrf')
        self.assertEqual(response.body, 'foo')

    def test_set_user_cookie(self):
        response = self.fetch('/set_user_cookie')
        cookie = response.headers['Set-Cookie']
        self.assertIn('httponly;', cookie)
        self.assertIn('user="', cookie)

    @mock.patch.object(UserStore, 'get')
    @mock.patch.object(jwt, 'decode')
    def test_get_user_cookie(self, mock_decode, mock_get):
        mock_decode.return_value = {
            'userName': 'fg',
            'uuid': '19836e2f-0f90-4644-a985-41367fde00e3',
        }
        mock_get.return_value = gen.maybe_future(mock.Mock())
        response = self.fetch('/get_user_cookie', headers={'Cookie': 'user=fg'})
        self.assertEqual(response.body,
                         "{'userName': 'fg', 'uuid': '19836e2f-0f90-4644-a985-41367fde00e3'}")
