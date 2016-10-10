from __future__ import absolute_import

from tornado.gen import coroutine

from bootcamp.services.user_service import UserService
from .base import BaseHandler


class UsersHandler(BaseHandler):
    @coroutine
    def get(self):
        service = UserService()
        titles = yield service.get_users()
        self.write('Number of titles: {}'.format(len(titles)))
