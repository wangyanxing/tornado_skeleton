from __future__ import absolute_import
import httplib
from tornado.gen import coroutine

from .base import BaseHandler


class HealthHandler(BaseHandler):
    @coroutine
    def get(self):
        """Return health of service."""
        self.set_status(httplib.OK)
        self.write('OK')
