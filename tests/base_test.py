import contextlib

from bootcamp.lib import database
from bootcamp.models.base import Model
from tornado.testing import AsyncTestCase


class BaseTestCase(AsyncTestCase):
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
