import httplib
import json
import urllib

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.tag import Tag
from bootcamp.services.tag_service import TagService
from doubles import allow_constructor, expect, patch_class
import mock
import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.tags.TagService'
    mock_service = TagService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_tags(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get_all.and_return_future([])

    response = yield http_client.fetch(base_url + '/api/tags')
    data = json.loads(response.body)
    assert data['tags'] == []
    assert data['status'] == 'ok'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_tag_by_name(http_client, base_url):
    tag_entity = Tag(
            name='SLG',
        )
    tag = yield TagService().create_with_entity(tag_entity)

    mock_service = gen_mock_service()
    expect(mock_service).get_by_name.with_args(tag.name).and_return_future(tag)

    response = yield http_client.fetch(base_url + '/api/tags?name=' + tag.name)

    assert json.loads(response.body) == {"status": "ok", "tag": tag.to_dict()}
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_tag_by_name_not_existed(http_client, base_url):
    fake_tag_name = 'not found'
    mock_service = gen_mock_service()
    expect(mock_service).get_by_name.with_args(fake_tag_name).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/tags?name=' + urllib.quote(fake_tag_name))

    assert response.body == '{"status": "failed", "errorMessage": "Not found."}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_create_tag(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_return_future(
        mock.Mock(uuid=fake_uuid),
    )

    body = r'name=ARPG'
    response = yield http_client.fetch(base_url + '/api/tags', method='POST', body=body)

    assert response.body == '{"status": "ok", "uuid": "' + fake_uuid + '"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_create_star_already_exists(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_raise(
        EntityAlreadyExistsError,
    )
    body = r'name=ARPG'
    response = yield http_client.fetch(base_url + '/api/tags', method='POST', body=body)

    assert response.body == '{"status": "failed", "errorMessage": "Tag name ARPG exist."}'
    assert response.code == httplib.OK
