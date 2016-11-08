import httplib
import json

from bootcamp.services.title_service import TitleService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.titles_by_tag.TitleService'
    mock_service = TitleService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_titles_by_tag(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    mock_service = gen_mock_service()
    expect(mock_service).get_all_by_tag.with_args(fake_uuid).and_return_future([])

    response = yield http_client.fetch(base_url + '/api/titles/tag/' + fake_uuid)
    result_object = json.loads(response.body)
    assert result_object['titles'] == []
    assert result_object['status'] == 'ok'
    assert response.code == httplib.OK
