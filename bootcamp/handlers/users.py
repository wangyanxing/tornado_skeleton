from __future__ import absolute_import

import json

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.user import User
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UsersHandler(BaseHandler):
    @coroutine
    def get(self):
        service = UserService()
        users = yield service.get_all()
        self.write('{' + '"users": {}'.format(json.dumps([user.to_dict() for user in users])) + '}')

    @coroutine
    def post(self):
        user_name = self.get_body_argument('user_name')
        password = self.get_body_argument('password')
        email = self.get_body_argument('email')

        user = User(
            user_name=user_name,
            password=password,
            email=email
        )
        service = UserService()

        try:
            user = yield service.create_with_entity(user)
            self.write('Added {}'.format(user.uuid))
        except EntityAlreadyExistsError:
            self.write('User name {} exist.'.format(user_name))
