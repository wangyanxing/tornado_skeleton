import httplib
import json
import urllib

from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.user import User
from bootcamp.services.user_service import UserService
from doubles import allow_constructor, expect, patch_class
import mock
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

    response = yield http_client.fetch(base_url + '/api/users')
    assert response.body == '{"status": "ok", "users": []}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_user_by_name(http_client, base_url):
    user_entity = User(
            user_name='fgbyname',
            password='fgdsb',
            email='fgdsb@fgdsb'
        )
    user = yield UserService().create_with_entity(user_entity)

    mock_service = gen_mock_service()
    expect(mock_service).get_by_name.with_args(user.user_name).and_return_future(user)

    response = yield http_client.fetch(base_url + '/api/users?user_name=' + user.user_name)

    assert json.loads(response.body) == {"status": "ok", "user": user.to_dict()}
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_get_user_by_name_not_existed(http_client, base_url):
    fake_user_name = 'not found'
    mock_service = gen_mock_service()
    expect(mock_service).get_by_name.with_args(fake_user_name).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/users?user_name=' + urllib.quote(fake_user_name))

    assert response.body == '{"status": "failed", "errorMessage": "Not found."}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_create_user(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_return_future(
        mock.Mock(uuid=fake_uuid),
    )

    body = r'user_name=fgdsb789&password=123&email=fgasdf&btn_submit=Submit'
    response = yield http_client.fetch(base_url + '/api/users', method='POST', body=body)

    assert response.body == '{"status": "ok", "uuid": "' + fake_uuid + '"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_add_user_already_exists(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_raise(
        EntityAlreadyExistsError,
    )
    body = r'user_name=fgdsb789&password=123&email=fgasdf&btn_submit=Submit'
    response = yield http_client.fetch(base_url + '/api/users', method='POST', body=body)

    assert response.body == '{"status": "failed", "errorMessage": "User name fgdsb789 exist."}'
    assert response.code == httplib.OK
