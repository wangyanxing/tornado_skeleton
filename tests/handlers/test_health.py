import httplib
import pytest


@pytest.mark.gen_test
def test_health(http_client, base_url):
    response = yield http_client.fetch(base_url + '/health')
    assert response.body == 'OK'
    assert response.code == httplib.OK
