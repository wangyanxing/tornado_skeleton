from __future__ import absolute_import

from tornado.gen import coroutine

from bootcamp.services.title_service import TitleService
from .base import BaseHandler


class TitlesHandler(BaseHandler):
    @coroutine
    def get(self):
        service = TitleService()
        titles = yield service.get_titles()
        self.write('Number of titles: {}'.format(len(titles)))
