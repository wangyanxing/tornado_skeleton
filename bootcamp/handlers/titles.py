from __future__ import absolute_import

from bootcamp.handlers.base import BaseHandler
from bootcamp.services.title_service import TitleService
from tornado.gen import coroutine


class TitlesHandler(BaseHandler):
    @coroutine
    def get(self):
        service = TitleService()
        titles = yield service.get_all()
        self.write('Number of titles: {}'.format(len(titles)))
