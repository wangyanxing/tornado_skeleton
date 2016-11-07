import httplib

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.services.tag_service import TagService
from doubles import allow_constructor, expect, patch_class
import mock
import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.add_tag.TagService'
    mock_service = TagService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_add_tag(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_return_future(
        mock.Mock(uuid=fake_uuid),
    )
    response = yield http_client.fetch(base_url + '/add_tag')
    assert response.body == 'Added {}'.format(fake_uuid)
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_add_tag_already_exists(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_raise(
        EntityAlreadyExistsError,
    )
    response = yield http_client.fetch(base_url + '/add_tag')
    assert response.body == 'Tag name SiFi exist.'
    assert response.code == httplib.OK
