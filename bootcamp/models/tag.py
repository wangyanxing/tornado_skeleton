import uuid

from bootcamp.models.base import Model
from sqlalchemy import (
    Column,
    Integer,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID


class Tag(Model):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID, default=lambda: str(uuid.uuid4()), nullable=False)  # pragma: no cover
    name = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
        }
