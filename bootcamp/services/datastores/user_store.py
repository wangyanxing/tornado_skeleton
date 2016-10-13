from bootcamp.lib.database import get_db_session
from bootcamp.models.user import User

from tornado.gen import coroutine


class UserStore(object):

    @coroutine
    def get_users(self):
        query = User.query()
        models = [_ for _ in query]
        return models

    @coroutine
    def get_user(self, uuid):
        query = User.query().filter(User.uuid == uuid)
        return query.first()

    @coroutine
    def get_user_by_name(self, user_name):
        query = User.query().filter(User.user_name == user_name)
        return query.first()

    @coroutine
    def create_from_entity(self, user):
        new_user = User(
            uuid=user.uuid,
            created_at=user.created_at,
            updated_at=user.updated_at,
            user_name=user.user_name,
            password=user.password,
            email=user.email
        )
        new_user.validate()
        new_user.persist()
        get_db_session().commit()
        return new_user
