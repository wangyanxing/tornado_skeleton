import uuid

from bootcamp.models.tag import Tag
from bootcamp.services.datastores.tag_store import TagStore
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTagStore(BaseTestCase):
    @gen_test
    def test_get_all(self):
        tags = yield TagStore().get_all()
        self.assertEquals(tags, [])

    @gen_test
    def test_get(self):
        fake_uuid = uuid.uuid4()
        tag = yield TagStore().get(str(fake_uuid))
        self.assertIsNone(tag)

    @gen_test
    def test_get_by_name(self):
        tag = yield TagStore().get_by_name('not found')
        self.assertIsNone(tag)

    @gen_test
    def test_create_from_entity(self):
        tag_entity = Tag(
            name='test',
        )
        new_tag = yield TagStore().create_from_entity(tag_entity)
        self.assertEquals(new_tag.name, tag_entity.name)

        tag = yield TagStore().get(new_tag.uuid)
        self.assertEquals(tag.name, new_tag.name)
