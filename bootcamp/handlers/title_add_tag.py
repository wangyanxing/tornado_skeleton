from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.title_service import TitleService

from tornado.gen import coroutine

from .base import BaseHandler


class TitleAddTagHandler(BaseHandler):
    @coroutine
    def get(self, title_uuid, tag_uuid):
        service = TitleService()

        self.set_header('Content-Type', 'application/json')

        try:
            if self.get_argument("add", 'n', True) == 'y':
                add = True
            else:
                add = False
            yield service.add_tag(title_uuid, tag_uuid, add)
            self.write({"status": "ok"})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "Title not found."})
