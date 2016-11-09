from __future__ import absolute_import

from bootcamp.handlers.base import BaseHandler
from bootcamp.services.title_service import TitleService
from tornado.gen import coroutine


class TitlesRecentHandler(BaseHandler):
    @coroutine
    def get(self):
        service = TitleService()

        self.set_header('Content-Type', 'application/json')

        titles = yield service.get_recentlly_added_titles(20)
        self.write({"status": "ok", "titles": [title.to_dict() for title in titles]})
