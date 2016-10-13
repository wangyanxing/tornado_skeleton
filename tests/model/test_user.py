import uuid

from bootcamp.models.user import User
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestUser(BaseTestCase):
    def setUp(self):
        self.user = User(
            id=1,
            uuid='1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            user_name='fg',
            password='fgdsb',
            email='fgdsb@fgdsb',
        )
        super(TestUser, self).setUp()

    @gen_test
    def test_to_dict(self):
        user = User(
            id=1,
            uuid='1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            user_name='fg',
            password='fgdsb',
            email='fgdsb@fgdsb',
        )
        expected = {
            'id': 1,
            'uuid': '1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            'userName': 'fg',
            'password': 'fgdsb',
            'email': 'fgdsb@fgdsb',
        }
        assert user.to_dict() == expected

    def test_create(self):
        self.save(self.user)
        db_user = User.get(self.user.uuid)
        self.assertIsNotNone(db_user)

    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            user = User(
                uuid=str(uuid.uuid4()),
                user_name=None,  # Should not be None
                password='fgdsb',
                email='fgdsb@fgdsb',
            )
            self.save(user)
