import uuid

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.base import Base
from bootcamp.services.datastores.star_store import StarStore

import mock
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestStarStore(BaseTestCase):
    @gen_test
    def test_get_all(self):
        stars = yield StarStore().get_all()
        self.assertEquals(stars, [])

    @gen_test
    def test_get(self):
        fake_uuid = uuid.uuid4()
        star = yield StarStore().get(str(fake_uuid))
        self.assertIsNone(star)

    @gen_test
    def test_get_by_name(self):
        star = yield StarStore().get_by_name('not found')
        self.assertIsNone(star)

    @gen_test
    def test_create_from_entity(self):
        star_entity = self.fixture_with_new_uuid('star')
        new_star = yield StarStore().create_from_entity(star_entity)
        self.assertEquals(new_star.name, star_entity.name)

        star = yield StarStore().get(new_star.uuid)
        self.assertEquals(star.name, star_entity.name)

    @gen_test
    def test_get_all_by_uuids(self):
        stars = yield StarStore().get_all_by_uuids([])
        self.assertEquals(stars, [])

    @mock.patch.object(Base, 'get')
    @gen_test
    def test_update_not_exists_entity(self, mock_get):
        mock_get.return_value = None

        fake_uuid = 'c736b780-11b6-4190-8529-4d89504b76a0'

        with self.assertRaises(ResourceNotFoundError):
            yield StarStore().update(fake_uuid, {})

        mock_get.assert_called_once_with(fake_uuid)
