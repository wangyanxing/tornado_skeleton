import uuid
import mock
from bootcamp.services.datastores.title_store import TitleStore
from bootcamp.services.title_service import TitleService
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test

from bootcamp.models.title import Title


class TestTitleService(BaseTestCase):
    @mock.patch.object(TitleStore, 'create_from_entity')
    @mock.patch.object(TitleService, 'handle_title_added')
    @gen_test
    def test_create_title_with_entity(self, mock_handle_added, mock_create):
        fake_title = mock.Mock(
            uuid=uuid.uuid4(),
            title_id='ABC-123',
            title='test title 1',
        )
        mock_create.return_value = gen.maybe_future(fake_title)
        mock_handle_added.return_value = gen.maybe_future(None)

        title_entity = Title(
            title_id='ABC-123',
            title='test title 1',
            video_path='test',
            file_names='test file',
            description='test des',
            video_size=1000000000,
            rate=8,
        )
        title = yield TitleService().create_title_with_entity(title_entity)

        mock_create.assert_called_once_with(title_entity)
        mock_handle_added.assert_called_once_with(fake_title)

        self.assertEquals(title.title, title_entity.title)
        self.assertEquals(title.title_id, title_entity.title_id)

    @mock.patch.object(TitleStore, 'get_title')
    @gen_test
    def test_get_title(self, mock_get):
        fake_title = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_title)

        fake_uuid = uuid.uuid4()
        title = yield TitleService().get_title(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        self.assertEquals(title, fake_title)

    @mock.patch.object(TitleStore, 'get_titles')
    @gen_test
    def test_get_titles(self, mock_get):
        fake_title = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_title)

        title = yield TitleService().get_titles()

        mock_get.assert_called_once_with()
        self.assertEquals(title, fake_title)
