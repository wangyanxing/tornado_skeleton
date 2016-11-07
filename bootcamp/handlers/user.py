from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UserHandler(BaseHandler):
    @coroutine
    def get(self, id):
        service = UserService()

        self.set_header('Content-Type', 'application/json')

        try:
            user = yield service.get(id)
            self.write({'status': 'ok', 'result': user.to_dict()})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "Not found."})
