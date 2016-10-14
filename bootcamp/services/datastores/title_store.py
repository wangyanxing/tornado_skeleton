from bootcamp.models.title import Title
from bootcamp.services.datastores.base_store import BaseStore

from tornado.gen import coroutine


class TitleStore(BaseStore):
    def __init__(self):
        super(TitleStore, self).__init__(Title)

    @coroutine
    def get_by_id(self, title_id):
        query = Title.query().filter(Title.title_id == title_id)
        return query.first()
