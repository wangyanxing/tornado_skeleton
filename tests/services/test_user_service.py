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

    @gen_test
    def test_like_title(self):
        user = yield UserService().create_with_entity(self.fixture_with_new_uuid('user'))
        title_uuid = '210eb8b3-9b82-4762-add9-0727dc2bcc99'
        self.assertTrue(user.liked_titles[title_uuid])

        yield UserService().like_title(
            user.uuid,
            title_uuid,
            False,
        )

        user = yield UserService().get(user.uuid)
        self.assertFalse(user.liked_titles[title_uuid])

    @gen_test
    def test_like_star(self):
        user = yield UserService().create_with_entity(self.fixture_with_new_uuid('user'))
        star_uuid = '24c8cf4b-b551-4bef-95fe-30e2a6749929'
        self.assertTrue(user.liked_stars[star_uuid])

        yield UserService().like_star(
            user.uuid,
            star_uuid,
            False,
        )

        user = yield UserService().get(user.uuid)
        self.assertFalse(user.liked_stars[star_uuid])
