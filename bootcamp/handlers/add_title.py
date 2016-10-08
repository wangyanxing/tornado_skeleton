from __future__ import absolute_import

from tornado.gen import coroutine

from .base import BaseHandler


class AddTitleHandler(BaseHandler):
    @coroutine
    def get(self):
        """Say hello!"""
        self.write('Hello bootcamper!')
