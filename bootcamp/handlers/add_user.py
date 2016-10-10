from __future__ import absolute_import

from tornado.gen import coroutine

from bootcamp.models.user import User
from bootcamp.services.user_service import UserService
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
        user = yield service.create_user_with_entity(user)
        self.write('Added {}'.format(user.uuid))