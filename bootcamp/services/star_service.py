from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.services import logger
from bootcamp.services.datastores.star_store import StarStore

from tornado.gen import coroutine, Return


class StarService(object):
    def __init__(self):
        self.store = StarStore()

    @coroutine
    def create_star_with_entity(self, star_entity):
        star_entity.validate()

        star = yield self.store.create_from_entity(star_entity)
        logger.info(
            dict(
                uuid=star.uuid,
                raw_name=star.raw_name,
                method='create_store_with_entity',
            )
        )
        yield self.handle_star_added(star)
        raise Return(star)

    @coroutine
    def handle_star_added(self, star):
        pass

    @coroutine
    def get_star(self, star_uuid):
        log_info = dict(
            uuid=star_uuid,
            method='get_star',
        )

        star = yield self.store.get_star(star_uuid)
        if not star:
            log_info.update({'error': 'star not found'})
            logger.exception(log_info)
            raise ResourceNotFoundError(log_info.get('error'))

        logger.info(log_info)
        raise Return(star)

    @coroutine
    def get_star_by_name(self, star_raw_name):
        log_info = dict(
            raw_name=star_raw_name,
            method='get_star_by_name',
        )

        star = yield self.store.get_star_by_name(star_raw_name)
        if not star:
            log_info.update({'result': 'star not found'})
            logger.info(log_info)
            raise Return(None)

        logger.info(log_info)
        raise Return(star)

    @coroutine
    def get_stars(self):
        star = yield self.store.get_stars()
        logger.info(
            dict(
                method='get_stars',
            )
        )
        raise Return(star)
