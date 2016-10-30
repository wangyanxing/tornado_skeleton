from __future__ import absolute_import

import json

from bootcamp.handlers.base import BaseHandler
from bootcamp.services.star_service import StarService
from tornado.gen import coroutine


class StarsHandler(BaseHandler):
    @coroutine
    def get(self):
        service = StarService()
        stars = yield service.get_all()
        result = [star.to_dict() for star in stars]
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(result))
