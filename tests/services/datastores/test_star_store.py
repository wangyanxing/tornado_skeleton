import uuid

from bootcamp.models.star import Star
from bootcamp.services.datastores.star_store import StarStore
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
        star_entity = Star(
            raw_name='test',
            hiragana='test2',
            english_id='test_2',
        )
        new_star = yield StarStore().create_from_entity(star_entity)
        self.assertEquals(new_star.raw_name, star_entity.raw_name)

        star = yield StarStore().get(new_star.uuid)
        self.assertEquals(star.raw_name, new_star.raw_name)
