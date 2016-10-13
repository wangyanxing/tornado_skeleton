from __future__ import absolute_import

from bootcamp.handlers.base import BaseHandler
from bootcamp.services.star_service import StarService
from tornado.gen import coroutine


class StarsHandler(BaseHandler):
    @coroutine
    def get(self):
        service = StarService()
        stars = yield service.get_stars()
        self.write('Number of stars: {}'.format(len(stars)))
