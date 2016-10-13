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
        star = yield self.store.get_star(star_uuid)
        raise Return(star)

    @coroutine
    def get_stars(self):
        star = yield self.store.get_stars()
        raise Return(star)
