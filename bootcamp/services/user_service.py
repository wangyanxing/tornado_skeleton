from bootcamp.lib.exceptions import ResourceNotFoundError
from bootcamp.lib.validation import is_valid_uuid_string
from bootcamp.services import logger
from bootcamp.services.base_service import BaseService
from bootcamp.services.datastores.title_store import TitleStore
from bootcamp.services.datastores.user_store import UserStore

from tornado.gen import coroutine, Return


class UserService(BaseService):
    def __init__(self):
        super(UserService, self).__init__()
        self.store = UserStore()
        self.title_store = TitleStore()

    @coroutine
    def get_by_name(self, user_name):
        user = yield self.store.get_by_name(user_name)

        logger.info(dict(
            user_name=user_name,
            method='get_by_name',
            result_uuid=None if not user else user.uuid,
        ))
        raise Return(user)

    @coroutine
    def check_duplicates(self, entity):
        user = yield self.get_by_name(entity.user_name)
        raise Return(user is not None)

    @coroutine
    def like_title(self, user_uuid, title_uuid, like):
        user_uuid = is_valid_uuid_string(user_uuid)
        title_uuid = is_valid_uuid_string(title_uuid)

        update_dict = {'liked_titles': {}}
        update_dict['liked_titles'][title_uuid] = like
        self.store.update(user_uuid, update_dict)

        logger.info(dict(
            user_uuid=user_uuid,
            title_uuid=title_uuid,
            like=like,
            method='like_title',
        ))
        raise Return()

    @coroutine
    def like_star(self, user_uuid, star_uuid, like):
        user_uuid = is_valid_uuid_string(user_uuid)
        star_uuid = is_valid_uuid_string(star_uuid)

        update_dict = {'liked_stars': {}}
        update_dict['liked_stars'][star_uuid] = like
        self.store.update(user_uuid, update_dict)

        logger.info(dict(
            user_uuid=user_uuid,
            star_uuid=star_uuid,
            like=like,
            method='like_star',
        ))
        raise Return()

    @coroutine
    def get_all_liked_titles(self, user_uuid):
        log_info = dict(
            user_uuid=user_uuid,
            method='get_all_liked_titles',
        )

        user_uuid = is_valid_uuid_string(user_uuid)

        user = yield self.store.get(user_uuid)
        if not user:
            log_info.update({'error': 'user not found'})
            logger.exception(log_info)
            raise ResourceNotFoundError(log_info.get('error'))

        title_uuids = list(user.liked_titles)

        titles = yield self.title_store.get_all_by_uuids(title_uuids)

        logger.info(log_info)
        raise Return(titles)
