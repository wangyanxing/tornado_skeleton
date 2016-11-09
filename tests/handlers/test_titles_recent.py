import httplib
import json

from bootcamp.services.title_service import TitleService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.titles_recent.TitleService'
    mock_service = TitleService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_titles_recent(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get_recentlly_added_titles.and_return_future([])

    response = yield http_client.fetch(base_url + '/api/titles/recent')
    result_object = json.loads(response.body)
    assert result_object['titles'] == []
    assert result_object['status'] == 'ok'
    assert response.code == httplib.OK
