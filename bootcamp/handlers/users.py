from __future__ import absolute_import

import urllib

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.user import User
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UsersHandler(BaseHandler):
    @coroutine
    def get(self):
        service = UserService()

        if not self.get_argument("user_name", None, True):
            users = yield service.get_all()
            self.write({"status": "ok", "users": [user.to_dict() for user in users]})
        else:
            user_name = self.get_argument("user_name", None, True)
            user = yield service.get_by_name(urllib.unquote(user_name))
            if not user:
                self.write({"status": "failed", "errorMessage": "Not found."})
            else:
                self.write({'status': 'ok', 'user': user.to_dict()})

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
            self.write({"status": "ok", "uuid": user.uuid})
        except EntityAlreadyExistsError:
            self.write({"status": "failed", "errorMessage": "User name {} exist.".format(user_name)})
