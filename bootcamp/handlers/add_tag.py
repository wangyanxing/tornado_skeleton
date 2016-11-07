from __future__ import absolute_import

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.tag import Tag
from bootcamp.services.tag_service import TagService

from tornado.gen import coroutine

from .base import BaseHandler


class AddTagHandler(BaseHandler):
    @coroutine
    def get(self):
        tag_entity = Tag(
            name='SiFi',
        )
        service = TagService()

        try:
            tag = yield service.create_with_entity(tag_entity)
            self.write('Added {}'.format(tag.uuid))
        except EntityAlreadyExistsError:
            self.write('Tag name {} exist.'.format(tag_entity.name))
