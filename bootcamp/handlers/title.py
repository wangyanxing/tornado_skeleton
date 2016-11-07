from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.title_service import TitleService

from tornado.gen import coroutine

from .base import BaseHandler


class TitleHandler(BaseHandler):
    @coroutine
    def get(self, id):
        service = TitleService()

        self.set_header('Content-Type', 'application/json')

        try:
            title = yield service.get(id)
            self.write({'status': 'ok', 'title': title.to_dict()})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "Not found."})
