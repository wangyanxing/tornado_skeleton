from bootcamp.services import logger
from bootcamp.services.base_service import BaseService
from bootcamp.services.datastores.tag_store import TagStore

from tornado.gen import coroutine, Return


class TagService(BaseService):
    def __init__(self):
        super(TagService, self).__init__()
        self.store = TagStore()

    @coroutine
    def get_by_name(self, tag_name):
        log_info = dict(
            tag_name=tag_name,
            method='get_by_name',
        )

        tag = yield self.store.get_by_name(tag_name)
        if not tag:
            log_info.update({'result': 'tag not found'})
            logger.info(log_info)
            raise Return(None)

        logger.info(log_info)
        raise Return(tag)

    @coroutine
    def check_duplicates(self, entity):
        tag = yield self.get_by_name(entity.name)
        raise Return(tag is not None)
