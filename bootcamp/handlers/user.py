from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UserHandler(BaseHandler):
    @coroutine
    def get(self, id):
        service = UserService()
        try:
            user = yield service.get(id)
            self.write(user.to_dict())
        except ResourceNotFoundError:
            self.write('Not found')
