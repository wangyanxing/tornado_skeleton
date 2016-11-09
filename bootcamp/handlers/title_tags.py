from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.title_service import TitleService

from tornado.gen import coroutine

from .base import BaseHandler


class TitleTagsHandler(BaseHandler):
    @coroutine
    def get(self, id):
        service = TitleService()

        self.set_header('Content-Type', 'application/json')

        try:
            tags = yield service.get_tags_by_title(id)
            self.write({"status": "ok", "tags": [tag.to_dict() for tag in tags]})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "Title not found."})
