from bootcamp.services.datastores.title_store import TitleStore
from bootcamp.services.title_service import TitleService
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestTitleService(BaseTestCase):
    @mock.patch.object(TitleStore, 'get_by_id')
    @gen_test
    def test_get_title_by_id(self, mock_get):
        fake_title = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_title)

        fake_title_id = 'ABC-123'
        title = yield TitleService().get_by_id(fake_title_id)

        mock_get.assert_called_once_with(fake_title_id)
        self.assertEquals(title, fake_title)

    @mock.patch.object(TitleStore, 'get_by_id')
    @gen_test
    def test_check_duplicates(self, mock_get):
        fake_title = mock.Mock(title_id='ABC-123')
        mock_get.return_value = gen.maybe_future(fake_title)

        dup = yield TitleService().check_duplicates(fake_title)

        mock_get.assert_called_once_with('ABC-123')
        self.assertTrue(dup)
