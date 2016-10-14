from bootcamp.services import logger
from bootcamp.services.base_service import BaseService
from bootcamp.services.datastores.user_store import UserStore

from tornado.gen import coroutine, Return


class UserService(BaseService):
    def __init__(self):
        super(UserService, self).__init__()
        self.store = UserStore()

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
