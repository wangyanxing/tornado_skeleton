import uuid

from bootcamp.models.user import User
from bootcamp.services.datastores.user_store import UserStore
from bootcamp.services.user_service import UserService
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestUserService(BaseTestCase):
    @mock.patch.object(UserStore, 'create_from_entity')
    @mock.patch.object(UserService, 'handle_user_added')
    @gen_test
    def test_create_user_with_entity(self, mock_handle_added, mock_create):
        fake_user = mock.Mock(
            uuid=uuid.uuid4(),
            user_name='fg',
            email='fgdsb@fgdsb',
        )
        mock_create.return_value = gen.maybe_future(fake_user)
        mock_handle_added.return_value = gen.maybe_future(None)

        user_entity = User(
            user_name='fg',
            password='fgdsb',
            email='fgdsb@fgdsb',
        )
        user = yield UserService().create_user_with_entity(user_entity)

        mock_create.assert_called_once_with(user_entity)
        mock_handle_added.assert_called_once_with(fake_user)

        self.assertEquals(user.user_name, user_entity.user_name)
        self.assertEquals(user.email, user_entity.email)

    @mock.patch.object(UserStore, 'get_user')
    @gen_test
    def test_get_user(self, mock_get):
        fake_user = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_user)

        fake_uuid = uuid.uuid4()
        user = yield UserService().get_user(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        self.assertEquals(user, fake_user)

    @mock.patch.object(UserStore, 'get_users')
    @gen_test
    def test_get_users(self, mock_get):
        fake_user = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_user)

        user = yield UserService().get_users()

        mock_get.assert_called_once_with()
        self.assertEquals(user, fake_user)

    @mock.patch.object(UserStore, 'is_user_exist')
    @gen_test
    def test_is_user_exist(self, mock_exist):
        mock_exist.return_value = gen.maybe_future(False)

        exist = yield UserService().is_user_exist('fg')
        self.assertEquals(exist, False)
