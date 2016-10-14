from bootcamp.models.star import Star
from bootcamp.services.datastores.base_store import BaseStore

from tornado.gen import coroutine


class StarStore(BaseStore):
    def __init__(self):
        super(StarStore, self).__init__(Star)

    @coroutine
    def get_by_name(self, raw_name):
        query = self.model_class.query().filter(self.model_class.raw_name == raw_name)
        return query.first()
