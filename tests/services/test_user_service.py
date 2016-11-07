from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.user import User
from bootcamp.services.datastores.base_store import BaseStore
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

    @mock.patch.object(BaseStore, 'get')
    @mock.patch.object(BaseStore, 'get_all_by_uuids')
    @gen_test
    def test_get_all_liked_titles(self, mock_get_all_by_uuids, mock_get):
        fake_uuid = 'c736b780-11b6-4190-8529-4d89504b76a0'
        fake_user = User(
            liked_titles={
              '210eb8b3-9b82-4762-add9-0727dc2bcc99': True
            }
        )

        fake_titles = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_user)
        mock_get_all_by_uuids.return_value = gen.maybe_future(fake_titles)

        titles = yield UserService().get_all_liked_titles(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        mock_get_all_by_uuids.assert_called_once_with(['210eb8b3-9b82-4762-add9-0727dc2bcc99'])
        self.assertEquals(titles, fake_titles)

    @mock.patch.object(BaseStore, 'get')
    @mock.patch.object(BaseStore, 'get_all_by_uuids')
    @gen_test
    def test_get_no_liked_titles(self, mock_get_all_by_uuids, mock_get):
        fake_uuid = 'c736b780-11b6-4190-8529-4d89504b76a0'
        fake_user = User(
            liked_titles={}
        )
        fake_titles = []

        mock_get.return_value = gen.maybe_future(fake_user)
        mock_get_all_by_uuids.return_value = gen.maybe_future(fake_titles)

        titles = yield UserService().get_all_liked_titles(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        mock_get_all_by_uuids.assert_called_once_with([])
        self.assertEquals(titles, fake_titles)

    @mock.patch.object(BaseStore, 'get')
    @gen_test
    def test_get_all_liked_titles_user_not_found(self, mock_get):
        mock_get.return_value = gen.maybe_future(None)

        fake_uuid = 'c736b780-11b6-4190-8529-4d89504b76a0'

        with self.assertRaises(ResourceNotFoundError):
            yield UserService().get_all_liked_titles(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)

    @mock.patch.object(BaseStore, 'get')
    @mock.patch.object(BaseStore, 'get_all_by_uuids')
    @gen_test
    def test_get_all_liked_stars(self, mock_get_all_by_uuids, mock_get):
        fake_uuid = 'c736b780-11b6-4190-8529-4d89504b76a0'
        fake_user = User(
            liked_stars={
              '210eb8b3-9b82-4762-add9-0727dc2bcc99': True
            }
        )

        fake_stars = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_user)
        mock_get_all_by_uuids.return_value = gen.maybe_future(fake_stars)

        stars = yield UserService().get_all_liked_stars(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        mock_get_all_by_uuids.assert_called_once_with(['210eb8b3-9b82-4762-add9-0727dc2bcc99'])
        self.assertEquals(stars, fake_stars)

    @mock.patch.object(BaseStore, 'get')
    @mock.patch.object(BaseStore, 'get_all_by_uuids')
    @gen_test
    def test_get_no_liked_stars(self, mock_get_all_by_uuids, mock_get):
        fake_uuid = 'c736b780-11b6-4190-8529-4d89504b76a0'
        fake_user = User(
            liked_stars={}
        )

        fake_stars = []
        mock_get.return_value = gen.maybe_future(fake_user)
        mock_get_all_by_uuids.return_value = gen.maybe_future(fake_stars)

        stars = yield UserService().get_all_liked_stars(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        mock_get_all_by_uuids.assert_called_once_with([])
        self.assertEquals(stars, fake_stars)

    @mock.patch.object(BaseStore, 'get')
    @gen_test
    def test_get_all_liked_stars_user_not_found(self, mock_get):
        mock_get.return_value = gen.maybe_future(None)

        fake_uuid = 'c736b780-11b6-4190-8529-4d89504b76a0'

        with self.assertRaises(ResourceNotFoundError):
            yield UserService().get_all_liked_stars(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
