import pytest


@pytest.mark.gen_test
def test_slash(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.body == 'Hello bootcamper!'
