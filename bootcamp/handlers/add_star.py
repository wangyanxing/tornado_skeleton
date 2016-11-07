from __future__ import absolute_import

from bootcamp.models.star import Star
from bootcamp.services.star_service import StarService

from tornado.gen import coroutine

from .base import BaseHandler


class AddStarHandler(BaseHandler):
    @coroutine
    def get(self):
        star = Star(
            name='fg',
            hiragana='fgdsb',
            english_id='fgdsb'
        )
        service = StarService()

        star = yield service.create_with_entity(star)
        self.write('Added {}'.format(star.uuid))
