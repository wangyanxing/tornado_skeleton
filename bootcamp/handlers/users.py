from __future__ import absolute_import

from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UsersHandler(BaseHandler):
    @coroutine
    def get(self):
        service = UserService()
        titles = yield service.get_users()
        self.write('Number of titles: {}'.format(len(titles)))
