import contextlib

from bootcamp.lib import database
from bootcamp.models.base import Model
from charlatan import FixturesManagerMixin
from tests.conftest import fixtures_manager
from tornado.testing import AsyncTestCase


class BaseTestCase(AsyncTestCase, FixturesManagerMixin):
    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.fixtures_manager = fixtures_manager

    def tearDown(self):
        for engine_type in database.sessions:
            database.sessions[engine_type].remove()
        engine = database.get_db_engine('write')
        with contextlib.closing(engine.connect()) as connection:
            transaction = connection.begin()
            for table in reversed(Model.metadata.sorted_tables):
                connection.execute(table.delete())
            transaction.commit()

    def save(self, model):
        database.get_db_session('write').add(model)
        database.get_db_session('write').commit()
        database.get_db_session('read').expunge_all()
