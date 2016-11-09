import httplib

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.title import Title
from bootcamp.services.title_service import TitleService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.title_tags.TitleService'
    mock_service = TitleService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_title_tags(http_client, base_url):
    title_entity = Title(
            title_id='titleTags',
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
    expect(mock_service).get_tags_by_title.and_return_future([])

    response = yield http_client.fetch(base_url + '/api/titles/' + title.uuid + '/tags')
    assert response.body == '{"status": "ok", "tags": []}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_title_tags_title_not_existed(http_client, base_url):
    fake_uuid = 'a9ab843d-4300-4ade-8c57-f5669b5bad31'
    mock_service = gen_mock_service()
    expect(mock_service).get_tags_by_title.and_raise(
        ResourceNotFoundError,
    )

    response = yield http_client.fetch(base_url + '/api/titles/' + fake_uuid + '/tags')
    assert response.body == '{"status": "failed", "errorMessage": "Title not found."}'
    assert response.code == httplib.OK
