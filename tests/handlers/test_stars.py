import httplib

from bootcamp.services.star_service import StarService
from doubles import allow_constructor, expect, patch_class
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

    response = yield http_client.fetch(base_url + '/stars')
    assert response.body == 'Number of stars: 0'
    assert response.code == httplib.OK
