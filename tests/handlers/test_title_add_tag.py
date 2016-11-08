import httplib

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.tag import Tag
from bootcamp.models.title import Title
from bootcamp.services.tag_service import TagService
from bootcamp.services.title_service import TitleService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.title_add_tag.TitleService'
    mock_service = TitleService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_title_add_tag(http_client, base_url):
    title_entity = Title(
            title_id='AddTag',
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

    tag_entity = Tag(
            name='SPG',
        )
    tag = yield TagService().create_with_entity(tag_entity)

    mock_service = gen_mock_service()
    expect(mock_service).add_tag.with_args(title.uuid, tag.uuid, True).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/titles/' + title.uuid + '/add_tag/' + tag.uuid + '?add=y')
    assert response.body == '{"status": "ok"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_title_remove_tag(http_client, base_url):
    title_entity = Title(
            title_id='RemoveTag',
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

    tag_entity = Tag(
            name='PUZ',
        )
    tag = yield TagService().create_with_entity(tag_entity)

    mock_service = gen_mock_service()
    expect(mock_service).add_tag.with_args(title.uuid, tag.uuid, False).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/titles/' + title.uuid + '/add_tag/' + tag.uuid + '?add=n')
    assert response.body == '{"status": "ok"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_title_add_tag_title_not_existed(http_client, base_url):
    fake_uuid = 'a9ab843d-4300-4ade-8c57-f5669b5bad31'
    mock_service = gen_mock_service()
    expect(mock_service).add_tag.and_raise(
        ResourceNotFoundError,
    )

    response = yield http_client.fetch(base_url + '/api/titles/' + fake_uuid + '/add_tag/' + fake_uuid + '?add=y')
    assert response.body == '{"status": "failed", "errorMessage": "Title not found."}'
    assert response.code == httplib.OK
