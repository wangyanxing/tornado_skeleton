from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.user_service import UserService

from tornado.gen import coroutine

from .base import BaseHandler


class UserLikeTitlesHandler(BaseHandler):
    @coroutine
    def get(self, user_uuid):
        service = UserService()
        try:
            titles = yield service.get_all_liked_titles(user_uuid)
            self.write({"status": "ok", "titles": [title.to_dict() for title in titles]})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "User not found."})
