from bootcamp.services.datastores.title_store import TitleStore
from bootcamp.services.title_service import TitleService
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestTitleService(BaseTestCase):
    @mock.patch.object(TitleStore, 'get_by_id')
    @gen_test
    def test_get_title_by_id(self, mock_get):
        fake_title = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_title)

        fake_title_id = 'ABC-123'
        title = yield TitleService().get_by_id(fake_title_id)

        mock_get.assert_called_once_with(fake_title_id)
        self.assertEquals(title, fake_title)

    @mock.patch.object(TitleStore, 'get_by_id')
    @gen_test
    def test_check_duplicates(self, mock_get):
        fake_title = mock.Mock(title_id='ABC-123')
        mock_get.return_value = gen.maybe_future(fake_title)

        dup = yield TitleService().check_duplicates(fake_title)

        mock_get.assert_called_once_with('ABC-123')
        self.assertTrue(dup)

    @gen_test
    def test_add_new_tag(self):
        title = yield TitleService().create_with_entity(self.fixture_with_new_uuid('title'))
        tag_uuids = ['c736b780-11b6-4190-8529-4d89504b76a0', 'efc5907c-7316-4a36-a910-044c18e39d10']
        add_tag_uuid = 'efc5907c-11b6-4a36-8529-044c18e39d10'
        self.assertEquals(len(title.tags), 2)
        self.assertEquals(title.tags[0], tag_uuids[0])
        self.assertEquals(title.tags[1], tag_uuids[1])

        yield TitleService().add_tag(
            title.uuid,
            add_tag_uuid,
            True,
        )

        title = yield TitleStore().get(title.uuid)
        self.assertEquals(len(title.tags), 3)
        self.assertTrue(title.tags[2] == add_tag_uuid)

    @gen_test
    def test_add_existed_tag(self):
        title = yield TitleService().create_with_entity(self.fixture_with_new_uuid('title'))
        tag_uuids = ['c736b780-11b6-4190-8529-4d89504b76a0', 'efc5907c-7316-4a36-a910-044c18e39d10']
        add_tag_uuid = tag_uuids[1]
        self.assertEquals(len(title.tags), 2)
        self.assertEquals(title.tags[0], tag_uuids[0])
        self.assertEquals(title.tags[1], tag_uuids[1])

        yield TitleService().add_tag(
            title.uuid,
            add_tag_uuid,
            True,
        )

        title = yield TitleStore().get(title.uuid)
        self.assertEquals(len(title.tags), 2)

    @gen_test
    def test_remove_existed_tag(self):
        title = yield TitleService().create_with_entity(self.fixture_with_new_uuid('title'))
        tag_uuids = ['c736b780-11b6-4190-8529-4d89504b76a0', 'efc5907c-7316-4a36-a910-044c18e39d10']
        remove_tag_uuid = tag_uuids[0]
        self.assertEquals(len(title.tags), 2)
        self.assertEquals(title.tags[0], tag_uuids[0])
        self.assertEquals(title.tags[1], tag_uuids[1])

        yield TitleService().add_tag(
            title.uuid,
            remove_tag_uuid,
            False,
        )

        title = yield TitleService().get(title.uuid)
        self.assertEquals(len(title.tags), 1)
        self.assertEquals(title.tags[0], tag_uuids[1])

    @gen_test
    def test_remove_not_existed_tag(self):
        title = yield TitleService().create_with_entity(self.fixture_with_new_uuid('title'))
        remove_tag_uuid = 'efc5907c-11b6-4a36-8529-044c18e39d10'

        self.assertEquals(len(title.tags), 2)

        yield TitleService().add_tag(
            title.uuid,
            remove_tag_uuid,
            False,
        )

        title = yield TitleService().get(title.uuid)
        self.assertEquals(len(title.tags), 2)
