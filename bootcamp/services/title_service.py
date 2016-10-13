from bootcamp.lib.exceptions import EntityAlreadyExistsError, ResourceNotFoundError
from bootcamp.services import logger
from bootcamp.services.datastores.title_store import TitleStore

from tornado.gen import coroutine, Return


class TitleService(object):
    def __init__(self):
        self.store = TitleStore()

    @coroutine
    def create_title_with_entity(self, title_entity):
        title_entity.validate()

        log_info = dict(
            uuid=title_entity.uuid,
            title_id=title_entity.title_id,
            method='create_title_with_entity',
        )

        # Check duplicates
        title = yield self.get_title_by_id(title_entity.title_id)
        if title:
            log_info.update({'error': 'title_id already exists'})
            logger.exception(log_info)
            raise EntityAlreadyExistsError(log_info.get('error'))

        title = yield self.store.create_from_entity(title_entity)
        logger.info(log_info)

        yield self.handle_title_added(title)
        raise Return(title)

    @coroutine
    def handle_title_added(self, title):
        pass

    @coroutine
    def get_title(self, title_uuid):
        log_info = dict(
            title_uuid=title_uuid,
            method='get_title',
        )

        title = yield self.store.get_title(title_uuid)
        if not title:
            log_info.update({'error': 'title not found'})
            logger.exception(log_info)
            raise ResourceNotFoundError(log_info.get('error'))

        logger.info(log_info)
        raise Return(title)

    @coroutine
    def get_titles(self):
        title = yield self.store.get_titles()

        logger.info(dict(
            method='get_titles',
            num_titles=len(title),
        ))
        raise Return(title)

    @coroutine
    def get_title_by_id(self, title_id):
        title = yield self.store.get_title_by_id(title_id)

        logger.info(dict(
            title_id=title_id,
            method='get_title_by_id',
            result_uuid=None if not title else title.uuid,
        ))
        raise Return(title)
