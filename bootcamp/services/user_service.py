from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.services import logger
from bootcamp.services.datastores.user_store import UserStore

from tornado.gen import coroutine, Return


class UserService(object):
    def __init__(self):
        self.store = UserStore()

    @coroutine
    def create_user_with_entity(self, user_entity):
        user_entity.validate()

        log_info = dict(
            uuid=user_entity.uuid,
            user_name=user_entity.user_name,
            method='create_user_with_entity',
        )

        # Check duplicates
        user = yield self.get_user_by_name(user_entity.user_name)
        if user:
            log_info.update({'error': 'user_name already exists'})
            logger.exception(log_info)
            raise EntityAlreadyExistsError(log_info.get('error'))

        user = yield self.store.create_from_entity(user_entity)
        logger.info(log_info)

        yield self.handle_user_added(user)
        raise Return(user)

    @coroutine
    def handle_user_added(self, user):
        pass

    @coroutine
    def get_user(self, user_uuid):
        user = yield self.store.get_user(user_uuid)
        raise Return(user)

    @coroutine
    def get_users(self):
        users = yield self.store.get_users()
        raise Return(users)

    @coroutine
    def get_user_by_name(self, user_name):
        user = yield self.store.get_user_by_name(user_name)

        logger.info(dict(
            user_name=user_name,
            method='get_user_by_name',
            result_uuid=None if not user else user.uuid,
        ))
        raise Return(user)
