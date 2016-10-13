import uuid

from bootcamp.models.star import Star
from bootcamp.services.datastores.star_store import StarStore
import mock
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestStarStore(BaseTestCase):
    @mock.patch.object(Star, 'query')
    @gen_test
    def test_get_stars(self, mock_query):
        mock_query.return_value = [1, 2, 3]

        stars = yield StarStore().get_stars()

        mock_query.assert_called_once_with()
        self.assertEquals(stars, [1, 2, 3])

    @gen_test
    def test_get_star(self):
        fake_uuid = uuid.uuid4()
        star = yield StarStore().get_star(fake_uuid)
        self.assertIsNotNone(star)

    @mock.patch.object(Star, 'persist')
    @mock.patch('bootcamp.lib.database.get_db_session')
    @gen_test
    def test_create_from_entity(self, mock_get_db, mock_persist):
        star_entity = Star(
            raw_name='test',
            english_name='test2',
        )
        mock_persist.return_value = None
        mock_get_db.return_value = mock.Mock()

        yield StarStore().create_from_entity(star_entity)

        mock_persist.assert_called_once_with()
