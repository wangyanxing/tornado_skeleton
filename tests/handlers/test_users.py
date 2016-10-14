import httplib

from bootcamp.services.user_service import UserService
from doubles import allow_constructor, expect, patch_class
import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.users.UserService'
    mock_service = UserService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_users(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).get_all.and_return_future([])

    response = yield http_client.fetch(base_url + '/users')
    assert response.body == 'Number of users: 0'
    assert response.code == httplib.OK
