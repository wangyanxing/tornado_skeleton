from __future__ import absolute_import

from bootcamp.models.user import User
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class AddUserHandler(BaseHandler):
    @coroutine
    def get(self):
        user = User(
            user_name='fg',
            password='fgdsb',
            email='fgdsb@fgdsb'
        )
        service = UserService()
        is_user_exist = yield service.is_user_exist(user.user_name)

        if is_user_exist:
            self.write('User name {} exist.'.format(user.user_name))
        else:
            user = yield service.create_user_with_entity(user)
            self.write('Added {}'.format(user.uuid))
