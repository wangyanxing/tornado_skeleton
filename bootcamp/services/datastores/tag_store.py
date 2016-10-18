from bootcamp.models.tag import Tag
from bootcamp.services.datastores.base_store import BaseStore

from tornado.gen import coroutine


class TagStore(BaseStore):
    def __init__(self):
        super(TagStore, self).__init__(Tag)

    @coroutine
    def get_by_name(self, name):
        query = self.model_class.query().filter(self.model_class.name == name)
        return query.first()
