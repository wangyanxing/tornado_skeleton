from bootcamp.lib.database import get_db_session
from bootcamp.models.star import Star

from tornado.gen import coroutine


class StarStore(object):

    @coroutine
    def get_stars(self):
        query = Star.query()
        return query.all()

    @coroutine
    def get_star(self, uuid):
        query = Star.query().filter(Star.uuid == uuid)
        return query.first()

    @coroutine
    def get_star_by_name(self, raw_name):
        query = Star.query().filter(Star.raw_name == raw_name)
        return query.first()

    @coroutine
    def create_from_entity(self, entity):
        new_star = Star(
            uuid=entity.uuid,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            raw_name=entity.raw_name,
            english_name=entity.english_name,
            pronunciation=entity.pronunciation,
        )
        new_star.validate()
        new_star.persist()
        get_db_session().commit()
        return new_star
