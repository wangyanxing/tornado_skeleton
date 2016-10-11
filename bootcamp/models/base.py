import datetime

from bootcamp.lib.camel_case import snake_to_camel
from bootcamp.lib.database import get_db_session
import pytz
from sqlalchemy import Column, DateTime, event
from sqlalchemy.ext import declarative
from voluptuous import Required, Schema


class Base(object):  # pragma: no cover
    created_at = Column(DateTime, default=datetime.datetime.utcnow,
                        nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=lambda: datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
                        nullable=True)

    @classmethod
    def query(cls):
        return get_db_session().query(cls)

    def to_dict(self):
        raise NotImplementedError

    @classmethod
    def get(cls, id_):
        q = cls.query().filter_by(id=id_)
        return q.first()

    def persist(self):
        get_db_session().add(self)

    def update(self, attrs):
        for key in attrs:
            if not hasattr(self, key):
                raise AttributeError()
            setattr(self, key, attrs[key])
        return self

    def validate(self):
        if hasattr(self, 'validation_schema'):
            schema = self.convert_model_schema()
            validation_attrs = {attr: getattr(self, attr) for attr in self.validation_schema}
            filtered_attrs = Schema(schema)(validation_attrs)
            for attr, value in filtered_attrs.iteritems():
                setattr(self, attr, value)

    def convert_model_schema(self, camel_case=False, input_schema=None):
        input_schema = input_schema or self.validation_schema
        return Base.format_schema(input_schema, camel_case)

    @classmethod
    def format_schema(cls, input_schema, camel_case=False):
        schema = {}
        for field_name, schema_info in input_schema.iteritems():
            if camel_case:
                field_name = snake_to_camel(field_name)
            validators = schema_info.get('validators')
            if schema_info.get('required'):
                required_error = schema_info.get('required_error', 'errors.is.required')
                schema[Required(field_name, msg=required_error)] = validators
            else:
                schema[field_name] = validators
        return schema


Model = declarative.declarative_base(cls=Base)


def validate(mapper, connection, instance):  # pragma: no cover
    instance.validate()


event.listen(Model, 'before_insert', validate, propagate=True)
event.listen(Model, 'before_update', validate, propagate=True)
