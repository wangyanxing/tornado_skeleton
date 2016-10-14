import uuid

from bootcamp.models.user import User
from bootcamp.services.datastores.user_store import UserStore
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestUserStore(BaseTestCase):
    @gen_test
    def test_get_all(self):
        users = yield UserStore().get_all()
        self.assertEquals(users, [])

    @gen_test
    def test_get(self):
        fake_uuid = uuid.uuid4()
        user = yield UserStore().get(str(fake_uuid))
        self.assertIsNone(user)

    @gen_test
    def test_create_from_entity(self):
        user_entity = User(
            user_name='fg',
            password='fgdsb',
            email='fgdsb@fgdsb',
        )
        new_user = yield UserStore().create_from_entity(user_entity)
        self.assertEquals(user_entity.user_name, user_entity.user_name)

        user = yield UserStore().get(user_entity.uuid)
        self.assertEquals(user.user_name, new_user.user_name)

        user = yield UserStore().get_by_name(new_user.user_name)
        self.assertEquals(user.uuid, new_user.uuid)
