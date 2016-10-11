from bootcamp.bootcamp import make_app

import pytest


@pytest.fixture
def app():
    return make_app()
