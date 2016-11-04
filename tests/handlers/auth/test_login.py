import httplib
import json

from bootcamp.services.user_service import UserService
from doubles import allow_constructor, expect, patch_class
import mock
import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.auth.login.UserService'
    mock_service = UserService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_login(http_client, base_url):
    fake_uuid = '05bf9bc2-a418-404b-9b15-c8670407a8bf'
    fake_password = 'fgdsb'
    mock_service = gen_mock_service()
    expect(mock_service).get_by_name.and_return_future(
        mock.Mock(uuid=fake_uuid, password=fake_password),
    )
    response = yield http_client.fetch(
        base_url + '/auth/login',
        method='POST',
        headers={'Content-Type': 'application/json'},
        body='{"username":"fg","password":"fgdsb"}'
    )

    data = json.loads(response.body)
    assert data.get('token') is not None
    assert data.get('result') == 'Success'
    assert response.code == httplib.OK
