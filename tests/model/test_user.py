from bootcamp.models.user import User
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestUser(BaseTestCase):
    def setUp(self):
        super(TestUser, self).setUp()
        self.user = self.fixture_with_new_uuid('user')

    @gen_test
    def test_to_dict(self):
        expected = {
            'uuid': self.user.uuid,
            'userName': 'fg',
            'password': 'fgdsb',
            'email': 'fgdsb@fgdsb',
            'likedTitles': {
                '210eb8b3-9b82-4762-add9-0727dc2bcc99': True
            },
            'playTimes': {
                '210eb8b3-9b82-4762-add9-0727dc2bcc99': 2
            },
        }
        assert self.user.to_dict() == expected

    @gen_test
    def test_create(self):
        self.save(self.user)
        db_user = User.get(self.user.uuid)
        self.assertIsNotNone(db_user)

    @gen_test
    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            user = self.fixture_with_new_uuid('user_invalid')
            self.save(user)
