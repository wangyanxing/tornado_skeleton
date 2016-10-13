import uuid

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.star import Star
from bootcamp.services.datastores.star_store import StarStore
from bootcamp.services.star_service import StarService
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestStarService(BaseTestCase):
    @mock.patch.object(StarStore, 'create_from_entity')
    @mock.patch.object(StarService, 'handle_star_added')
    @gen_test
    def test_create_star_with_entity(self, mock_handle_added, mock_create):
        fake_star = mock.Mock(
            uuid=uuid.uuid4(),
            raw_name='NAME',
            english_name='name',
        )
        mock_create.return_value = gen.maybe_future(fake_star)
        mock_handle_added.return_value = gen.maybe_future(None)

        star_entity = Star(
            raw_name='NAME',
            english_name='name',
        )
        star = yield StarService().create_star_with_entity(star_entity)

        mock_create.assert_called_once_with(star_entity)
        mock_handle_added.assert_called_once_with(fake_star)

        self.assertEquals(star.raw_name, star_entity.raw_name)
        self.assertEquals(star.english_name, star_entity.english_name)

    @mock.patch.object(StarStore, 'get_star')
    @gen_test
    def test_get_star(self, mock_get):
        fake_star = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_star)

        fake_uuid = uuid.uuid4()
        star = yield StarService().get_star(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        self.assertEquals(star, fake_star)

    @mock.patch.object(StarStore, 'get_star')
    @gen_test
    def test_get_star_not_found(self, mock_get):
        mock_get.return_value = gen.maybe_future(None)

        fake_uuid = uuid.uuid4()

        with self.assertRaises(ResourceNotFoundError):
            yield StarService().get_star(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)

    @mock.patch.object(StarStore, 'get_star_by_name')
    @gen_test
    def test_get_star_by_name(self, mock_get):
        fake_star = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_star)

        fake_name = 'abc'
        star = yield StarService().get_star_by_name(fake_name)

        mock_get.assert_called_once_with(fake_name)
        self.assertEquals(star, fake_star)

    @mock.patch.object(StarStore, 'get_star_by_name')
    @gen_test
    def test_get_star_by_name_not_found(self, mock_get):
        mock_get.return_value = gen.maybe_future(None)

        fake_name = 'abc'
        star = yield StarService().get_star_by_name(fake_name)

        mock_get.assert_called_once_with(fake_name)
        self.assertIsNone(star)

    @mock.patch.object(StarStore, 'get_stars')
    @gen_test
    def test_get_stars(self, mock_get):
        fake_star = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_star)

        star = yield StarService().get_stars()

        mock_get.assert_called_once_with()
        self.assertEquals(star, fake_star)
