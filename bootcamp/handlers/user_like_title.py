from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UserLikeTitleHandler(BaseHandler):
    @coroutine
    def get(self, user_uuid, title_uuid):
        service = UserService()
        try:
            like = self.get_argument("like", True, True)
            if like == 'y':
                like = True
            else:
                like = False
            yield service.like_title(user_uuid, title_uuid, like)
            self.write({"status": "ok"})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "User not found."})
