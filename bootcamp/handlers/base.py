import binascii
import Cookie
import json
import uuid

from bootcamp.handlers import logger
from bootcamp.lib.constants import USER_COOKIE_EXPIRES_DAYS, USER_COOKIE_NAME
from bootcamp.lib.context_local import ContextLocal
from bootcamp.services.user_service import UserService
import jwt
from tornado import stack_context
from tornado.gen import coroutine, engine, Return
from tornado.web import RequestHandler

COOKIE_KEY_USER_UUID = 'uuid'
COOKIE_KEY_IS_SESSION = 'is_session_cookie'
COOKIE_HTTP_HEADER = 'Cookie'


class BaseContext(ContextLocal):
    def __init__(self, request):
        super(BaseContext, self).__init__()
        self.request = request
        self.user = None


class BaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass

    def set_cookie(self, *args, **kwargs):
        # kwargs.setdefault('secure', True)  # HTTPS only
        # kwargs.setdefault('httponly', True)  # Not accessible to javascript
        super(BaseHandler, self).set_cookie(*args, **kwargs)

    @property
    def xsrf_token(self):
        if not hasattr(self, '_xsrf_token'):
            token = self.get_cookie('_xsrf')
            if not token:
                token = binascii.b2a_hex(uuid.uuid4().bytes)
                self.set_cookie('_xsrf', token, expires_days=USER_COOKIE_EXPIRES_DAYS)
            self._xsrf_token = token
        return self._xsrf_token

    def get_user_cookie(self):
        user_cookie = self.get_secure_cookie(
            USER_COOKIE_NAME,
            max_age_days=USER_COOKIE_EXPIRES_DAYS,
        )
        if user_cookie:
            try:
                user_dict = json.loads(user_cookie)
            except ValueError:
                logger.warning('Not a valid user cookie: %s' % user_cookie)
                self.clear_cookie(USER_COOKIE_NAME)
                return None

            if COOKIE_KEY_USER_UUID not in user_dict:
                logger.warning('No enough fields in the user cookie: %s' % user_cookie)
            return user_dict
        else:
            cookie_header = self.request.headers.get(COOKIE_HTTP_HEADER, None)
            if cookie_header is None:
                logger.warning('Missing cookie in HTTP header')
            else:
                cookie = Cookie.SimpleCookie(cookie_header)
                token = cookie.get(USER_COOKIE_NAME)
                if not token:
                    logger.info(
                        'HTTP Cookie header exists, but does not contain a user cookie: %s' %
                        cookie_header)
                    return None

                user_dict = jwt.decode(token.value, 'secret')
                logger.info('Token found: %s' % json.dumps(user_dict))
                return user_dict
        return None

    def set_user_cookie(self, user_cookie_dict):
        expires_days = None if user_cookie_dict.get(
            COOKIE_KEY_IS_SESSION, False) else USER_COOKIE_EXPIRES_DAYS
        logger.info('Setting user cookie')
        self.set_secure_cookie(
            USER_COOKIE_NAME,
            json.dumps(user_cookie_dict),
            expires_days=expires_days,
        )

    @coroutine
    def get_user_from_cookie(self):
        user_cookie_dict = self.get_user_cookie()
        if user_cookie_dict is None:
            raise Return((None, None))

        user_uuid = user_cookie_dict.get(COOKIE_KEY_USER_UUID, None)
        if not user_uuid:
            logger.warning('No UUID found in the user cookie')
            self.clear_cookie(USER_COOKIE_NAME)
            raise Return((None, None))

        user = yield UserService().get(user_uuid)

        if user is None:
            logger.warning('User not found')
            self.clear_cookie(USER_COOKIE_NAME)
            raise Return((None, None))

        raise Return((user_cookie_dict, user))

    def _execute(self, transforms, *args, **kwargs):
        @engine
        def _execute_impl():
            user_cookie_dict, user = yield self.get_user_from_cookie()
            if user is not None:
                self.login_user(user, user_cookie_dict)
            super(BaseHandler, self)._execute(transforms, *args, **kwargs)

        with stack_context.StackContext(BaseContext(self.request)):
            _execute_impl()

    def login_user(self, user, user_cookie_dict):
        logger.info('Logging in user: %s' % user.uuid)
        self._current_user = user
        self.set_user_cookie(user_cookie_dict)

    def get_current_user(self):
        return self._current_user
