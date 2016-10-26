from bootcamp.lib.database import get_db_session
from tornado.gen import coroutine


class BaseStore(object):
    def __init__(self, model_class):
        self.model_class = model_class

    @coroutine
    def create_from_entity(self, entity):
        entity.validate()
        entity.persist()
        get_db_session().commit()
        return entity

    @coroutine
    def get(self, uuid):
        query = self.model_class.query().filter(self.model_class.uuid == uuid)
        return query.first()

    @coroutine
    def get_all(self):
        query = self.model_class.query()
        return query.all()

    @coroutine
    def update(self, uuid, update_dict):
        model = self.model_class.get(uuid)
        model = model.update(update_dict)
        model.persist()
        get_db_session().commit()
        return model

    @coroutine
    def get_all_by_uuids(self, uuids):
        query = self.model_class.query().filter(self.model_class.uuid.in_(uuids))
        return query.all()
