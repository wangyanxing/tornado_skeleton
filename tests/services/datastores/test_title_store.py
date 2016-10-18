import datetime
import uuid

from bootcamp.services.datastores.title_store import TitleStore
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTitleStore(BaseTestCase):
    @gen_test
    def test_get_all(self):
        titles = yield TitleStore().get_all()
        self.assertEquals(titles, [])

    @gen_test
    def test_get(self):
        fake_uuid = uuid.uuid4()
        title = yield TitleStore().get(str(fake_uuid))
        self.assertIsNone(title)

    @gen_test
    def test_create_from_entity(self):
        title_entity = self.fixture_with_new_uuid('title')

        new_title = yield TitleStore().create_from_entity(title_entity)
        self.assertEquals(new_title.title_id, title_entity.title_id)

        title = yield TitleStore().get(new_title.uuid)
        self.assertEquals(title.title_id, new_title.title_id)

        title = yield TitleStore().get_by_id(new_title.title_id)
        self.assertEquals(title.uuid, new_title.uuid)
        self.assertEquals(title.published_date, datetime.datetime(2007, 12, 5, 0, 0))
        self.assertEquals(title.tags, [
            'c736b780-11b6-4190-8529-4d89504b76a0',
            'efc5907c-7316-4a36-a910-044c18e39d10',
        ])
