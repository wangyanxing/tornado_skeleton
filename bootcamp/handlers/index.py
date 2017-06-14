from __future__ import absolute_import

from tornado.gen import coroutine

from .base import BaseHandler
import time


class IndexHandler(BaseHandler):
    @coroutine
    def get(self):
        """Say hello!"""
        print 'sleeping'
        time.sleep(5)
        print 'done'
        self.write('Hello bootcamper!')
