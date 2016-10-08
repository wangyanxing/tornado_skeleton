import datetime
import pytz
from clay_config import config
from sqlalchemy.ext import declarative
from sqlalchemy import Column, DateTime, event
from voluptuous import Required, Schema

from bootcamp.lib.camel_case import coerce_snakecase_to_camelcase
from bootcamp.lib.classproperty import classproperty
from bootcamp.lib.database import get_db_session

logger = config.get_logger(__name__)


class Base(object):
    created_at = Column(DateTime, default=datetime.datetime.utcnow,
                        nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=lambda: datetime.datetime.utcnow().replace(tzinfo=pytz.utc),
                        nullable=True)

    @classproperty
    @classmethod
    def sortable_columns(cls):
        """The column names upon which this model can be sorted.

        Override this in child classes for special behavior.
        """
        return [col.name for col in cls.__table__.columns]

    @classmethod
    def query(cls):
        return get_db_session().query(cls)

    def to_dict(self):
        """Dump this model as a dictionary.

        To be overridden in all child classes.
        """
        raise NotImplementedError

    def to_dict_admin(self):
        """Dump this model as a dictionary, adding additional data for admins

        If not specified, fall back to to_dict.
        To be overridden in all child classes.
        """
        return self.to_dict()

    @classmethod
    def all(cls):
        """Return all instances of this model."""
        q = cls.query()
        return q

    @classmethod
    def get(cls, id_):
        """Get a model by id."""
        q = cls.query().filter_by(id=id_)
        return q.first()

    def persist(self):
        """Add model to session explicitly"""
        get_db_session().add(self)

    def update(self, attrs):
        """Update the provided attributes for this model instance."""
        for key in attrs:
            if not hasattr(self, key):
                raise AttributeError()
            setattr(self, key, attrs[key])
        return self

    def validate(self):
        """Run the model's schema validation."""
        if hasattr(self, 'validation_schema'):
            schema = self.convert_model_schema()
            validation_attrs = {attr: getattr(self, attr) for attr in self.validation_schema}
            filtered_attrs = Schema(schema)(validation_attrs)
            for attr, value in filtered_attrs.iteritems():
                setattr(self, attr, value)

    def convert_model_schema(self, camel_case=False, input_schema=None):
        """Convert the model schema format to a voluptuous schema."""
        input_schema = input_schema or self.validation_schema
        return Base.format_schema(input_schema, camel_case)

    @classmethod
    def format_schema(cls, input_schema, camel_case=False):
        """Convert the model schema format to a voluptuous schema."""
        schema = {}
        for field_name, schema_info in input_schema.iteritems():
            if camel_case:
                field_name = coerce_snakecase_to_camelcase(field_name)
            validators = schema_info.get('validators')
            if schema_info.get('required'):
                required_error = schema_info.get('required_error', 'errors.is.required')
                schema[Required(field_name, msg=required_error)] = validators
            else:
                schema[field_name] = validators
        return schema


Model = declarative.declarative_base(cls=Base)


def validate(mapper, connection, instance):
    """Validate event calls model instance's validation method."""
    instance.validate()


event.listen(Model, 'before_insert', validate, propagate=True)
event.listen(Model, 'before_update', validate, propagate=True)
