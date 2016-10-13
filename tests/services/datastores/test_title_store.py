import uuid

from bootcamp.models.title import Title
from bootcamp.services.datastores.title_store import TitleStore
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTitleStore(BaseTestCase):
    @gen_test
    def test_get_titles(self):
        titles = yield TitleStore().get_titles()
        self.assertEquals(titles, [])

    @gen_test
    def test_get_title(self):
        fake_uuid = uuid.uuid4()
        title = yield TitleStore().get_title(str(fake_uuid))
        self.assertIsNone(title)

    @gen_test
    def test_create_from_entity(self):
        title_entity = Title(
            title_id='ABC-123',
            title='test title 1',
            video_path='test',
            file_names='test file',
            description='test des',
            video_size=1000000000,
            rate=8,
        )

        new_title = yield TitleStore().create_from_entity(title_entity)
        self.assertEquals(new_title.title_id, title_entity.title_id)

        title = yield TitleStore().get_title(new_title.uuid)
        self.assertEquals(title.title_id, title.title_id)
