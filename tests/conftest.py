from bootcamp.bootcamp import make_app
from charlatan import FixturesManager
from clay import config

import pytest

fixtures_manager = FixturesManager()


@pytest.fixture(scope='session', autouse=True)
def init_test():
    fixtures_manager.load(
        config.get('fixtures'),
        models_package='bootcamp.models',
    )


@pytest.fixture
def app():
    print 'making app'
    return make_app()
