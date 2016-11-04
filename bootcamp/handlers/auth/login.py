from __future__ import absolute_import

import json

from bootcamp.handlers import logger
from bootcamp.handlers.base import BaseHandler
from bootcamp.services.user_service import UserService
import jwt

from tornado.gen import coroutine


class LoginHandler(BaseHandler):
    @coroutine
    def post(self):
        data = json.loads(self.request.body)
        user_name = data.get('username')
        password = data.get('password')

        log_dict = {
            'request': data,
            'route': 'auth/login',
        }

        user = yield UserService().get_by_name(user_name)

        respond = {'result': 'Success'}
        if not user or user.password != password:
            self.set_status(403)
            respond['result'] = 'Failed'
            respond['reason'] = 'User not found' if not user else 'Password not match'
        else:
            token = jwt.encode({
                'userName': user_name,
                'uuid': user.uuid,
            }, 'secret', algorithm='HS256')
            respond['token'] = token

        log_dict.update({'respond': respond})
        logger.info(log_dict)
        self.write(respond)
