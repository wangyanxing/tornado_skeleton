import httplib

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.user import User
from bootcamp.services.user_service import UserService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.user_like_titles.UserService'
    mock_service = UserService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_user_like_titles(http_client, base_url):
    user_entity = User(
            user_name='fg_like_av',
            password='fgdsb',
            email='fgdsb@fgdsb'
        )
    user = yield UserService().create_with_entity(user_entity)

    mock_service = gen_mock_service()
    expect(mock_service).get_all_liked_titles.and_return_future([])

    response = yield http_client.fetch(base_url + '/api/users/' + user.uuid + '/like_titles')
    assert response.body == '{"status": "ok", "titles": []}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_user_like_titles_user_not_existed(http_client, base_url):
    fake_uuid = 'a9ab843d-4300-4ade-8c57-f5669b5bad31'
    mock_service = gen_mock_service()
    expect(mock_service).get_all_liked_titles.and_raise(
        ResourceNotFoundError,
    )

    response = yield http_client.fetch(base_url + '/api/users/' + fake_uuid + '/like_titles')
    assert response.body == '{"status": "failed", "errorMessage": "User not found."}'
    assert response.code == httplib.OK
