import httplib
import json

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.tag import Tag
from bootcamp.services.tag_service import TagService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.tag.TagService'
    mock_service = TagService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_get_tag(http_client, base_url):
    tag_entity = Tag(
            name='RPG',
        )
    tag = yield TagService().create_with_entity(tag_entity)

    mock_service = gen_mock_service()
    expect(mock_service).get.and_return_future(tag)

    response = yield http_client.fetch(base_url + '/api/tags/' + tag.uuid)

    result_object = json.loads(response.body)
    assert result_object['status'] == 'ok'
    assert result_object['tag'] == tag.to_dict()
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_tag_not_found(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get.and_raise(
        ResourceNotFoundError,
    )
    response = yield http_client.fetch(base_url + '/api/tags/a9ab843d-4300-4ade-8c57-f5669b5bad31')
    assert response.body == '{"status": "failed", "errorMessage": "Not found."}'
    assert response.code == httplib.OK
