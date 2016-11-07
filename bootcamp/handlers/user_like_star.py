from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UserLikeStarHandler(BaseHandler):
    @coroutine
    def get(self, user_uuid, star_uuid):
        service = UserService()

        self.set_header('Content-Type', 'application/json')

        try:
            if self.get_argument("like", 'n', True) == 'y':
                like = True
            else:
                like = False
            yield service.like_star(user_uuid, star_uuid, like)
            self.write({"status": "ok"})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "User not found."})
