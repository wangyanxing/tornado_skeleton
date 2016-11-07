from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.tag_service import TagService

from tornado.gen import coroutine

from .base import BaseHandler


class TagHandler(BaseHandler):
    @coroutine
    def get(self, id):
        service = TagService()

        self.set_header('Content-Type', 'application/json')

        try:
            tag = yield service.get(id)
            self.write({'status': 'ok', 'tag': tag.to_dict()})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "Not found."})
