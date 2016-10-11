import uuid

import mock
from bootcamp.models.title import Title
from bootcamp.services.datastores.title_store import TitleStore
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTitleStore(BaseTestCase):
    @mock.patch.object(Title, 'query')
    @gen_test
    def test_get_titles(self, mock_query):
        mock_query.return_value = [1, 2, 3]

        titles = yield TitleStore().get_titles()

        mock_query.assert_called_once_with()
        self.assertEquals(titles, [1, 2, 3])

    @gen_test
    def test_get_title(self):
        fake_uuid = uuid.uuid4()
        title = yield TitleStore().get_title(fake_uuid)
        self.assertIsNotNone(title)

    @mock.patch.object(Title, 'persist')
    @mock.patch('bootcamp.lib.database.get_db_session')
    @gen_test
    def test_create_from_entity(self, mock_get_db, mock_persist):
        title_entity = Title(
            title_id='ABC-123',
            title='test title 1',
            video_path='test',
            file_names='test file',
            description='test des',
            video_size=1000000000,
            rate=8,
        )
        mock_persist.return_value = None
        mock_get_db.return_value = mock.Mock()

        yield TitleStore().create_from_entity(title_entity)

        mock_persist.assert_called_once_with()
