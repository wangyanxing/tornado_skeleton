from tornado.gen import coroutine, Return

from bootcamp.services import logger
from bootcamp.services.datastores.title_store import TitleStore


class TitleService(object):
    def __init__(self):
        self.store = TitleStore()

    @coroutine
    def create_title_with_entity(self, title_entity):
        title_entity.validate()

        title = yield self.store.create_from_entity(title_entity)
        logger.info(
            dict(
                uuid=title.uuid,
                title_id=title.title_id,
                method='create_title_with_entity',
            )
        )
        yield self.handle_title_added(title)
        raise Return(title)

    @coroutine
    def handle_title_added(self, title):
        pass

    @coroutine
    def get_title(self, title_uuid):
        title = yield self.store.get_title(title_uuid)
        raise Return(title)

    @coroutine
    def get_titles(self):
        title = yield self.store.get_titles()
        raise Return(title)
