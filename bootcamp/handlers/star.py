from __future__ import absolute_import

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services.star_service import StarService

from tornado.gen import coroutine

from .base import BaseHandler


class StarHandler(BaseHandler):
    @coroutine
    def get(self, id):
        service = StarService()

        self.set_header('Content-Type', 'application/json')

        try:
            star = yield service.get(id)
            self.write({'status': 'ok', 'star': star.to_dict()})
        except ResourceNotFoundError:
            self.write({"status": "failed", "errorMessage": "Not found."})
