import httplib
import json

from bootcamp.services.title_service import TitleService
from doubles import allow_constructor, expect, patch_class
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

    response = yield http_client.fetch(base_url + '/titles')
    data = json.loads(response.body)
    assert data['titles'] == []
    assert data['status'] == 'ok'
    assert response.code == httplib.OK
