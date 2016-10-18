from bootcamp.models.star import Star
from bootcamp.services.datastores.base_store import BaseStore

from tornado.gen import coroutine


class StarStore(BaseStore):
    def __init__(self):
        super(StarStore, self).__init__(Star)

    @coroutine
    def get_by_name(self, name):
        query = self.model_class.query().filter(self.model_class.name == name)
        return query.first()
