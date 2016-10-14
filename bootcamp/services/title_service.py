from bootcamp.services import logger
from bootcamp.services.base_service import BaseService
from bootcamp.services.datastores.title_store import TitleStore

from tornado.gen import coroutine, Return


class TitleService(BaseService):
    def __init__(self):
        super(TitleService, self).__init__()
        self.store = TitleStore()

    @coroutine
    def get_by_id(self, title_id):
        title = yield self.store.get_by_id(title_id)

        logger.info(dict(
            title_id=title_id,
            method='get_by_id',
            result_uuid=None if not title else title.uuid,
        ))
        raise Return(title)

    @coroutine
    def check_duplicates(self, entity):
        title = yield self.get_by_id(entity.title_id)
        raise Return(title is not None)
