from __future__ import absolute_import

import random
import string

from bootcamp.handlers.base import BaseHandler
from bootcamp.models.star import Star
from bootcamp.services.star_service import StarService
from tornado.gen import coroutine


def gen_random_name():
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))


class AddStarHandler(BaseHandler):
    @coroutine
    def get(self):
        star = Star(
            raw_name=gen_random_name(),
            english_name=gen_random_name(),
        )
        service = StarService()
        star = yield service.create_with_entity(star)
        self.write('Added {}'.format(star.uuid))
        self.write('<br>')
        self.write('Name {}'.format(star.raw_name))
