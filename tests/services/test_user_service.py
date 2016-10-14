from bootcamp.services.datastores.user_store import UserStore
from bootcamp.services.user_service import UserService
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestUserService(BaseTestCase):
    @mock.patch.object(UserStore, 'get_by_name')
    @gen_test
    def test_get_by_name(self, mock_get):
        fake_user = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_user)

        fake_user_name = 'fg'
        user = yield UserService().get_by_name(fake_user_name)

        mock_get.assert_called_once_with(fake_user_name)
        self.assertEquals(user, fake_user)

    @mock.patch.object(UserStore, 'get_by_name')
    @gen_test
    def test_check_duplicates(self, mock_get):
        fake_user = mock.Mock(user_name='fgdsb')
        mock_get.return_value = gen.maybe_future(fake_user)

        dup = yield UserService().check_duplicates(fake_user)

        mock_get.assert_called_once_with('fgdsb')
        self.assertTrue(dup)
