import httplib
import json

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.star import Star
from bootcamp.services.star_service import StarService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.star.StarService'
    mock_service = StarService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_get_star(http_client, base_url):
    star_entity = Star(
            name='super-fg',
            hiragana='fgdsb',
            english_id='fgdsb',
            pronunciation='fg',
            other_names='fgdsb',
            num_titles=0,
        )
    star = yield StarService().create_with_entity(star_entity)

    mock_service = gen_mock_service()
    expect(mock_service).get.and_return_future(star)

    response = yield http_client.fetch(base_url + '/api/stars/' + star.uuid)

    result_object = json.loads(response.body)
    assert result_object['status'] == 'ok'
    assert result_object['star'] == star.to_dict()
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_star_not_found(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get.and_raise(
        ResourceNotFoundError,
    )
    response = yield http_client.fetch(base_url + '/api/stars/a9ab843d-4300-4ade-8c57-f5669b5bad31')
    assert response.body == '{"status": "failed", "errorMessage": "Not found."}'
    assert response.code == httplib.OK
