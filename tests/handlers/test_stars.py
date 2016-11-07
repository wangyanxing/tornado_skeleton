import httplib
import json
import urllib

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.star import Star
from bootcamp.services.star_service import StarService
from doubles import allow_constructor, expect, patch_class
import mock
import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.stars.StarService'
    mock_service = StarService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_stars(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get_all.and_return_future([])

    response = yield http_client.fetch(base_url + '/api/stars')
    data = json.loads(response.body)
    assert data['stars'] == []
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_star_by_name(http_client, base_url):
    star_entity = Star(
            name='super-star-fg',
            hiragana='fgdsb',
            english_id='fgdsb',
            pronunciation='fg',
            other_names='fgdsb',
            num_titles=0,
        )
    star = yield StarService().create_with_entity(star_entity)

    mock_service = gen_mock_service()
    expect(mock_service).get_by_name.with_args(star.name).and_return_future(star)

    response = yield http_client.fetch(base_url + '/api/stars?name=' + star.name)

    assert json.loads(response.body) == {"status": "ok", "star": star.to_dict()}
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_star_by_name_not_existed(http_client, base_url):
    fake_star_name = 'not found'
    mock_service = gen_mock_service()
    expect(mock_service).get_by_name.with_args(fake_star_name).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/stars?name=' + urllib.quote(fake_star_name))

    assert response.body == '{"status": "failed", "errorMessage": "Not found."}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_create_star(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_return_future(
        mock.Mock(uuid=fake_uuid),
    )

    body = r'name=fg-create&hiragana=123&english_id=12345&pronunciation=fengge&other_names=fgdsb&num_titles=0'
    response = yield http_client.fetch(base_url + '/api/stars', method='POST', body=body)

    assert response.body == '{"status": "ok", "uuid": "' + fake_uuid + '"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_create_star_already_exists(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_raise(
        EntityAlreadyExistsError,
    )
    body = r'name=fg-create&hiragana=123&english_id=12345&pronunciation=fengge&other_names=fgdsb&num_titles=0'
    response = yield http_client.fetch(base_url + '/api/stars', method='POST', body=body)

    assert response.body == '{"status": "failed", "errorMessage": "Star name fg-create exist."}'
    assert response.code == httplib.OK
