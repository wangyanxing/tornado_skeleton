from bootcamp.lib.exceptions import EntityAlreadyExistsError, ResourceNotFoundError
from bootcamp.services import logger
from bootcamp.services.datastores.base_store import BaseStore
from tornado.gen import coroutine, Return


class BaseService(object):
    def __init__(self):
        self.store = BaseStore(None)

    @coroutine
    def get_all(self):
        star = yield self.store.get_all()
        logger.info(dict(method='get_all'))
        raise Return(star)

    @coroutine
    def handle_added(self, star):
        pass

    @coroutine
    def create_with_entity(self, entity):
        entity.validate()

        log_info = dict(
            uuid=entity.uuid,
            method='create_with_entity',
        )

        duplicates = yield self.check_duplicates(entity)
        if duplicates:
            log_info.update({'error': 'entity already exists'})
            logger.exception(log_info)
            raise EntityAlreadyExistsError(log_info.get('error'))

        new_created = yield self.store.create_from_entity(entity)
        logger.info(log_info)

        yield self.handle_added(new_created)
        raise Return(new_created)

    @coroutine
    def get(self, uuid):
        log_info = dict(
            uuid=uuid,
            method='get',
        )

        star = yield self.store.get(uuid)
        if not star:
            log_info.update({'error': 'star not found'})
            logger.exception(log_info)
            raise ResourceNotFoundError(log_info.get('error'))

        logger.info(log_info)
        raise Return(star)

    @coroutine
    def check_duplicates(self, entity):
        return False
