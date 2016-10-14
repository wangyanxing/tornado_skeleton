from bootcamp.services import logger
from bootcamp.services.base_service import BaseService
from bootcamp.services.datastores.star_store import StarStore

from tornado.gen import coroutine, Return


class StarService(BaseService):
    def __init__(self):
        super(StarService, self).__init__()
        self.store = StarStore()

    @coroutine
    def get_by_name(self, star_raw_name):
        log_info = dict(
            raw_name=star_raw_name,
            method='get_by_name',
        )

        star = yield self.store.get_by_name(star_raw_name)
        if not star:
            log_info.update({'result': 'star not found'})
            logger.info(log_info)
            raise Return(None)

        logger.info(log_info)
        raise Return(star)
