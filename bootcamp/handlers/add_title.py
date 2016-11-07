from __future__ import absolute_import

import uuid

from bootcamp.handlers.base import BaseHandler
from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.title import Title
from bootcamp.services.title_service import TitleService
from tornado.gen import coroutine


class AddTitleHandler(BaseHandler):
    @coroutine
    def get(self):
        title_entity = Title(
            title_id='ABC-123',
            title='test title 1',
            video_path='test',
            file_names=['test file'],
            description='test des',
            stars=[str(uuid.uuid4())],
            video_size=1000000000,
            rate=8,
        )
        service = TitleService()
        try:
            title = yield service.create_with_entity(title_entity)
            self.write('Added {}'.format(title.uuid))
        except EntityAlreadyExistsError:
            self.write('{} already exists'.format(title_entity.title_id))
