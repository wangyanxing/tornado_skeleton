from __future__ import absolute_import

from bootcamp.lib.exceptions import EntityAlreadyExistsError
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
            english_id='fgdsb',
            pronunciation='fg',
            other_names='fgdsb',
            num_titles=0,
        )
        service = StarService()

        try:
            star = yield service.create_with_entity(star)
            self.write('Added {}'.format(star.uuid))
        except EntityAlreadyExistsError:
            self.write('Star name {} exist.'.format(star.name))
