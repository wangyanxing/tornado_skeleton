from bootcamp.services.datastores.star_store import StarStore
from bootcamp.services.star_service import StarService
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestStarService(BaseTestCase):
    @mock.patch.object(StarStore, 'get_by_name')
    @gen_test
    def test_get_by_name(self, mock_get):
        fake_star = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_star)

        fake_name = 'abc'
        star = yield StarService().get_by_name(fake_name)

        mock_get.assert_called_once_with(fake_name)
        self.assertEquals(star, fake_star)

    @mock.patch.object(StarStore, 'get_by_name')
    @gen_test
    def test_get_by_name_not_found(self, mock_get):
        mock_get.return_value = gen.maybe_future(None)

        fake_name = 'abc'
        star = yield StarService().get_by_name(fake_name)

        mock_get.assert_called_once_with(fake_name)
        self.assertIsNone(star)
