from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UserLikeStarsHandler(BaseHandler):
    @coroutine
    def get(self, user_uuid):
        service = UserService()
        try:
            stars = yield service.get_all_liked_stars(user_uuid)
            self.write({"status": "ok", "stars": [star.to_dict() for star in stars]})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "User not found."})
