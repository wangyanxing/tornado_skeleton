import pytest

from bootcamp.bootcamp import make_app


@pytest.fixture
def app():
    return make_app()
