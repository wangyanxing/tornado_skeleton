import httplib
import uuid

from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.models.title import Title
from bootcamp.models.user import User
from bootcamp.services.title_service import TitleService
from bootcamp.services.user_service import UserService
from doubles import allow_constructor, expect, patch_class

import pytest


@pytest.fixture
def gen_mock_service():
    class_name = 'bootcamp.handlers.user_like_title.UserService'
    mock_service = UserService()
    service_class = patch_class(class_name)
    allow_constructor(service_class).and_return(mock_service)
    return mock_service


@pytest.mark.gen_test
def test_user_like_title(http_client, base_url):
    user_entity = User(
            user_name='fg_like_this_video',
            password='fgdsb',
            email='fgdsb@fgdsb'
        )
    user = yield UserService().create_with_entity(user_entity)

    title_entity = Title(
            title_id='like',
            title='test title 1',
            video_path='test',
            file_names=['test file'],
            description='test des',
            stars=[str(uuid.uuid4())],
            video_size=1000000000,
            rate=8,
        )

    title = yield TitleService().create_with_entity(title_entity)

    mock_service = gen_mock_service()
    expect(mock_service).like_title.with_args(user.uuid, title.uuid, True).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/users/' + user.uuid + '/like_titles/' + title.uuid + '?like=y')
    assert response.body == '{"status": "ok"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_user_dislike_title(http_client, base_url):
    user_entity = User(
            user_name='fg_dislike_video',
            password='fgdsb',
            email='fgdsb@fgdsb'
        )
    user = yield UserService().create_with_entity(user_entity)

    title_entity = Title(
            title_id='dislike',
            title='test title 1',
            video_path='test',
            file_names=['test file'],
            description='test des',
            stars=[str(uuid.uuid4())],
            video_size=1000000000,
            rate=8,
        )

    title = yield TitleService().create_with_entity(title_entity)

    mock_service = gen_mock_service()
    expect(mock_service).like_title.with_args(user.uuid, title.uuid, False).and_return_future(None)

    response = yield http_client.fetch(base_url + '/api/users/' + user.uuid + '/like_titles/' + title.uuid + '?like=n')
    assert response.body == '{"status": "ok"}'
    assert response.code == httplib.OK


@pytest.mark.gen_test
def test_user_like_title_user_not_existed(http_client, base_url):
    fake_uuid = 'a9ab843d-4300-4ade-8c57-f5669b5bad31'
    mock_service = gen_mock_service()
    expect(mock_service).like_title.and_raise(
        ResourceNotFoundError,
    )

    response = yield http_client.fetch(base_url + '/api/users/' + fake_uuid + '/like_titles/' + fake_uuid + '?like=y')
    assert response.body == '{"status": "failed", "errorMessage": "User not found."}'
    assert response.code == httplib.OK
