from bootcamp.models.user import User
from bootcamp.services.datastores.base_store import BaseStore

from tornado.gen import coroutine


class UserStore(BaseStore):
    def __init__(self):
        super(UserStore, self).__init__(User)

    @coroutine
    def get_by_name(self, user_name):
        query = User.query().filter(User.user_name == user_name)
        return query.first()
