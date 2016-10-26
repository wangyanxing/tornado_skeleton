from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.lib.validation import is_valid_uuid_string
from bootcamp.services import logger
from bootcamp.services.base_service import BaseService
from bootcamp.services.datastores.tag_store import TagStore
from bootcamp.services.datastores.title_store import TitleStore

from tornado.gen import coroutine, Return


class TitleService(BaseService):
    def __init__(self):
        super(TitleService, self).__init__()
        self.store = TitleStore()
        self.tag_store = TagStore()

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

    @coroutine
    def add_tag(self, title_uuid, tag_uuid, add=True):
        title_uuid = is_valid_uuid_string(title_uuid)
        tag_uuid = is_valid_uuid_string(tag_uuid)

        title = yield self.store.get(title_uuid)

        tag_list = list(title.tags)
        if add is True:
            if tag_uuid not in tag_list:
                tag_list.append(tag_uuid)
        else:
            if tag_uuid in tag_list:
                tag_list.remove(tag_uuid)

        update_dict = {'tags': tag_list}
        self.store.update(title_uuid, update_dict)

        logger.info(dict(
            title_uuid=title_uuid,
            tag_uuid=tag_uuid,
            add=add,
            method='add_tag',
        ))
        raise Return()

    @coroutine
    def get_tags_by_title(self, title_uuid):
        log_info = dict(
            uuid=title_uuid,
            method='get_tags_by_title',
        )

        title_uuid = is_valid_uuid_string(title_uuid)

        title = yield self.store.get(title_uuid)
        if not title:
            log_info.update({'error': 'title not found'})
            logger.exception(log_info)
            raise ResourceNotFoundError(log_info.get('error'))

        tag_list = list(getattr(title, 'tags'))

        tags = yield self.tag_store.get_all_by_uuids(tag_list)
        logger.info(log_info)
        raise Return(tags)
