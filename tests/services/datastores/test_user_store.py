import uuid

from bootcamp.models.user import User
from bootcamp.services.datastores.user_store import UserStore
import mock
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestUserStore(BaseTestCase):
    @mock.patch.object(User, 'query')
    @gen_test
    def test_get_users(self, mock_query):
        mock_query.return_value = [1, 2, 3]

        users = yield UserStore().get_users()

        mock_query.assert_called_once_with()
        self.assertEquals(users, [1, 2, 3])

    @gen_test
    def test_get_user(self):
        fake_uuid = uuid.uuid4()
        user = yield UserStore().get_user(str(fake_uuid))
        self.assertIsNone(user)

    @mock.patch.object(User, 'persist')
    @mock.patch('bootcamp.lib.database.get_db_session')
    @gen_test
    def test_create_from_entity(self, mock_get_db, mock_persist):
        user_entity = User(
            user_name='fg',
            password='fgdsb',
            email='fgdsb@fgdsb',
        )
        mock_persist.return_value = None
        mock_get_db.return_value = mock.Mock()

        yield UserStore().create_from_entity(user_entity)

        mock_persist.assert_called_once_with()
