from tornado.testing import gen_test, AsyncTestCase

from bootcamp.models.user import User


class TestUser(AsyncTestCase):
    @gen_test
    def test_get(self):
        uuid = '1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4'
        obj = User.get(uuid)
        assert isinstance(obj, User) == False

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
