import httplib

import mock
import pytest
from doubles import allow_constructor, expect, patch_class

from bootcamp.services.title_service import TitleService


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.add_title.TitleService'
    mock_service = TitleService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_add_title(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    mock_service = gen_mock_service()
    expect(mock_service).create_title_with_entity.and_return_future(
        mock.Mock(uuid=fake_uuid),
    )
    response = yield http_client.fetch(base_url + '/add_title')
    assert response.body == 'Added {}'.format(fake_uuid)
    assert response.code == httplib.OK
