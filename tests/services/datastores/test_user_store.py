import uuid

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
        user_entity = self.fixture_with_new_uuid('user')
        new_user = yield UserStore().create_from_entity(user_entity)
        self.assertEquals(user_entity.user_name, user_entity.user_name)

        user = yield UserStore().get(user_entity.uuid)
        self.assertEquals(user.user_name, new_user.user_name)

        user = yield UserStore().get_by_name(new_user.user_name)
        self.assertEquals(user.uuid, new_user.uuid)

    @gen_test
    def test_json_column(self):
        user_entity = self.fixture_with_new_uuid('user')
        new_user = yield UserStore().create_from_entity(user_entity)
        self.assertTrue(new_user.liked_titles['210eb8b3-9b82-4762-add9-0727dc2bcc99'])

    @gen_test
    def test_get_all_by_uuids(self):
        users = yield UserStore().get_all_by_uuids([])
        self.assertEquals(users, [])

    @gen_test
    def test_get_latest_created(self):
        users = yield UserStore().get_latest_created(5)
        self.assertEquals(users, [])
