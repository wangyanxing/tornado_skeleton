from __future__ import absolute_import

import urllib

from bootcamp.handlers.base import BaseHandler
from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.star import Star
from bootcamp.services.star_service import StarService
from tornado.gen import coroutine


class StarsHandler(BaseHandler):
    @coroutine
    def get(self):
        service = StarService()

        self.set_header('Content-Type', 'application/json')

        if not self.get_argument("name", None, True):
            stars = yield service.get_all()
            self.write({"status": "ok", "stars": [star.to_dict() for star in stars]})
        else:
            star_name = self.get_argument("name", None, True)
            star = yield service.get_by_name(urllib.unquote(star_name))
            if not star:
                self.write({"status": "failed", "errorMessage": "Not found."})
            else:
                self.write({'status': 'ok', 'star': star.to_dict()})

    @coroutine
    def post(self):
        name = self.get_body_argument('name', None, True)
        hiragana = self.get_body_argument('hiragana', None, True)
        english_id = self.get_body_argument('english_id', None, True)
        pronunciation = self.get_body_argument('pronunciation', '', True)
        other_names = self.get_body_argument('other_names', '', True)
        num_titles = self.get_body_argument('num_titles', 0, True)

        star_entity = Star(
            name=name,
            hiragana=hiragana,
            english_id=english_id,
            pronunciation=pronunciation,
            other_names=other_names,
            num_titles=int(num_titles),
        )
        service = StarService()

        self.set_header('Content-Type', 'application/json')

        try:
            star = yield service.create_with_entity(star_entity)
            self.write({"status": "ok", "uuid": star.uuid})
        except EntityAlreadyExistsError:
            self.write({"status": "failed", "errorMessage": "Star name {} exist.".format(name)})
