from __future__ import absolute_import

import httplib

from bootcamp.handlers.base import BaseHandler
from tornado.gen import coroutine


class HealthHandler(BaseHandler):
    @coroutine
    def get(self):
        """Return health of service."""
        self.set_status(httplib.OK)
        self.write('OK')
