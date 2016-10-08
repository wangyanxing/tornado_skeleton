from __future__ import absolute_import

from tornado.gen import coroutine

from bootcamp.models.title import Title
from bootcamp.services.title_service import TitleService
from .base import BaseHandler


class AddTitleHandler(BaseHandler):
    @coroutine
    def get(self):
        title = Title(
            title_id='ABC-123',
            title='test title 1',
            video_path='test',
            file_names='test file',
            description='test des',
            video_size=1000000000,
            rate=8,
        )
        service = TitleService()
        title = yield service.create_title_with_entity(title)
        self.write('Added {}'.format(title.uuid))
