import uuid

from bootcamp.lib.exceptions import EntityAlreadyExistsError, ResourceNotFoundError
from bootcamp.services.base_service import BaseService
from bootcamp.services.datastores.base_store import BaseStore
import mock
from tests.base_test import BaseTestCase
from tornado import gen
from tornado.testing import gen_test


class TestBaseService(BaseTestCase):
    @mock.patch.object(BaseStore, 'create_from_entity')
    @mock.patch.object(BaseService, 'handle_added')
    @mock.patch.object(BaseService, 'check_duplicates')
    @gen_test
    def test_create_with_entity(self, mock_check, mock_handle_added, mock_create):
        fake_entity = mock.Mock(
            uuid=uuid.uuid4(),
        )
        mock_create.return_value = gen.maybe_future(fake_entity)
        mock_handle_added.return_value = gen.maybe_future(None)
        mock_check.return_value = gen.maybe_future(False)

        entity = yield BaseService().create_with_entity(fake_entity)

        mock_check.assert_called_once_with(fake_entity)
        mock_create.assert_called_once_with(fake_entity)
        mock_handle_added.assert_called_once_with(fake_entity)

        self.assertEquals(entity.uuid, fake_entity.uuid)

    @mock.patch.object(BaseStore, 'create_from_entity')
    @mock.patch.object(BaseService, 'check_duplicates')
    @gen_test
    def test_create_with_entity_already_exists(self, mock_check, mock_create):
        fake_entity = mock.Mock(
            uuid=uuid.uuid4(),
        )
        mock_create.return_value = gen.maybe_future(fake_entity)
        mock_check.return_value = gen.maybe_future(True)

        with self.assertRaises(EntityAlreadyExistsError):
            yield BaseService().create_with_entity(fake_entity)

        mock_check.assert_called_once_with(fake_entity)
        mock_create.assert_not_called()

    @mock.patch.object(BaseStore, 'get')
    @gen_test
    def test_get(self, mock_get):
        fake_entity = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_entity)

        fake_uuid = uuid.uuid4()
        entity = yield BaseService().get(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)
        self.assertEquals(entity, fake_entity)

    @mock.patch.object(BaseStore, 'get')
    @gen_test
    def test_get_not_found(self, mock_get):
        mock_get.return_value = gen.maybe_future(None)

        fake_uuid = uuid.uuid4()

        with self.assertRaises(ResourceNotFoundError):
            yield BaseService().get(fake_uuid)

        mock_get.assert_called_once_with(fake_uuid)

    @mock.patch.object(BaseStore, 'get_all')
    @gen_test
    def test_get_all(self, mock_get):
        fake_entity = mock.Mock()
        mock_get.return_value = gen.maybe_future(fake_entity)

        entity = yield BaseService().get_all()

        mock_get.assert_called_once_with()
        self.assertEquals(entity, fake_entity)

    @gen_test
    def test_check_duplicates(self):
        dup = yield BaseService().check_duplicates(None)
        self.assertFalse(dup)
