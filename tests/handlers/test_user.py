import httplib
import json

# from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.user import User
from bootcamp.services.user_service import UserService
from doubles import allow_constructor, patch_class
# from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.users.UserService'
    mock_service = UserService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_get_user(http_client, base_url):
    user_entity = User(
            user_name='fg',
            password='fgdsb',
            email='fgdsb@fgdsb'
        )
    user = yield UserService().create_with_entity(user_entity)

    response = yield http_client.fetch(base_url + '/api/users/' + user.uuid)
    print response.body
    assert json.loads(response.body) == user.to_dict()
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_user_not_found(http_client, base_url):
    # mock_service = gen_mock_service()
    # expect(mock_service).get.and_raise(
    #     ResourceNotFoundError,
    # )
    response = yield http_client.fetch(base_url + '/api/users/a9ab843d-4300-4ade-8c57-f5669b5bad31')
    assert response.body == 'Not found'
    assert response.code == httplib.OK
