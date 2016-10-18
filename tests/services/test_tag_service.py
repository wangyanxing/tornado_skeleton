from bootcamp.services.datastores.tag_store import TagStore
from bootcamp.services.tag_service import TagService
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestTagService(BaseTestCase):
    @mock.patch.object(TagStore, 'get_by_name')
    @gen_test
    def test_get_by_name(self, mock_get):
        fake_tag = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_tag)

        fake_name = 'abc'
        tag = yield TagService().get_by_name(fake_name)

        mock_get.assert_called_once_with(fake_name)
        self.assertEquals(tag, fake_tag)

    @mock.patch.object(TagStore, 'get_by_name')
    @gen_test
    def test_get_by_name_not_found(self, mock_get):
        mock_get.return_value = gen.maybe_future(None)

        fake_name = 'abc'
        tag = yield TagService().get_by_name(fake_name)

        mock_get.assert_called_once_with(fake_name)
        self.assertIsNone(tag)
