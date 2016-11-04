import httplib

from bootcamp.lib.exceptions import EntityAlreadyExistsError
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
    assert response.body == '{"users": []}'
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

    assert response.body == 'Added {}'.format(fake_uuid)
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_add_user_already_exists(http_client, base_url):
    mock_service = gen_mock_service()
    expect(mock_service).create_with_entity.and_raise(
        EntityAlreadyExistsError,
    )
    body = r'user_name=fgdsb789&password=123&email=fgasdf&btn_submit=Submit'
    response = yield http_client.fetch(base_url + '/api/users', method='POST', body=body)

    assert response.body == 'User name fgdsb789 exist.'
    assert response.code == httplib.OK
