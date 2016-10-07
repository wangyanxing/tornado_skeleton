from __future__ import absolute_import

from .base import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        """Say hello!"""
        self.write('Hello bootcamper!')
