from __future__ import absolute_import

from bootcamp.services.title_service import TitleService

from tornado.gen import coroutine

from .base import BaseHandler


class TitlesByTagHandler(BaseHandler):
    @coroutine
    def get(self, id):
        service = TitleService()

        self.set_header('Content-Type', 'application/json')

        titles = yield service.get_all_by_tag(id)
        self.write({"status": "ok", "titles": [title.to_dict() for title in titles]})
