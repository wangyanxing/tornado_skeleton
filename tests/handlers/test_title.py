import httplib
import json

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.title import Title
from bootcamp.services.title_service import TitleService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.title.TitleService'
    mock_service = TitleService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_get_tag(http_client, base_url):
    title_entity = Title(
            title_id='titleId',
            title='title',
            video_path='video_path',
            file_names=['file_names'],
            description='description',
            maker='maker',
            video_size=1000000,
            stars=[],
            rate=4.2,
            length=121,
            published_date='2011-01-29',
        )
    title = yield TitleService().create_with_entity(title_entity)

    mock_service = gen_mock_service()
    expect(mock_service).get.and_return_future(title)

    response = yield http_client.fetch(base_url + '/api/titles/' + title.uuid)

    result_object = json.loads(response.body)
    assert result_object['status'] == 'ok'
    assert result_object['title'] == title.to_dict()
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_tag_not_found(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get.and_raise(
        ResourceNotFoundError,
    )
    response = yield http_client.fetch(base_url + '/api/titles/a9ab843d-4300-4ade-8c57-f5669b5bad31')
    assert response.body == '{"status": "failed", "errorMessage": "Not found."}'
    assert response.code == httplib.OK
