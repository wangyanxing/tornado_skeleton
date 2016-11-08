import httplib
import json
import urllib

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.title import Title
from bootcamp.services.title_service import TitleService
from doubles import allow_constructor, expect, patch_class

import mock
import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.titles.TitleService'
    mock_service = TitleService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_titles(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get_all.and_return_future([])

    response = yield http_client.fetch(base_url + '/api/titles')
    result_object = json.loads(response.body)
    assert result_object['titles'] == []
    assert result_object['status'] == 'ok'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_title_by_id(http_client, base_url):
    title_entity = Title(
            title_id='titleId02',
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
    expect(mock_service).get_by_id.with_args(title.title_id).and_return_future(title)

    response = yield http_client.fetch(base_url + '/api/titles?id=' + title.title_id)

    assert json.loads(response.body) == {"status": "ok", "title": title.to_dict()}
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_title_by_id_not_existed(http_client, base_url):
    fake_title_id = 'not found'
    mock_service = gen_mock_service()
    expect(mock_service).get_by_id.with_args(fake_title_id).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/titles?id=' + urllib.quote(fake_title_id))

    assert response.body == '{"status": "failed", "errorMessage": "Not found."}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_create_title(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_return_future(
        mock.Mock(uuid=fake_uuid),
    )

    body = r'''title_id=FF15&title=RPG&video_path=tmp&file_names=["file"]
    &description=desc&maker=fg&video_size=100&rate=3.2&length=100&published_date=2011-01-10'''
    response = yield http_client.fetch(base_url + '/api/titles', method='POST', body=body)

    assert response.body == '{"status": "ok", "uuid": "' + fake_uuid + '"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_add_title_already_exists(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_raise(
        EntityAlreadyExistsError,
    )
    body = r'''title_id=FF15&title=RPG&video_path=tmp&file_names=["file"]
    &description=desc&maker=fg&video_size=100&rate=3.2&length=100&published_date=2011-01-10'''
    response = yield http_client.fetch(base_url + '/api/titles', method='POST', body=body)

    assert response.body == '{"status": "failed", "errorMessage": "Title title_id FF15 exist."}'
    assert response.code == httplib.OK
