import uuid

from tornado.gen import coroutine, Return

from bootcamp.services import logger
from bootcamp.services.datastores.user_store import UserStore


class UserService(object):
    def __init__(self):
        self.store = UserStore()

    @coroutine
    def create_user_with_entity(self, user_entity):
        if not user_entity.uuid:
            user_entity.uuid = str(uuid.uuid4())
        user_entity.validate()

        user = yield self.store.create_from_entity(user_entity)
        logger.info(
            dict(
                uuid=user.uuid,
                user_name=user.user_name,
                method='create_user_with_entity',
            )
        )
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
