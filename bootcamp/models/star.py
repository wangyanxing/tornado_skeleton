import uuid

from bootcamp.models.base import Model
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID


class Star(Model):
    __tablename__ = 'stars'

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID, default=lambda: str(uuid.uuid4()), nullable=False)  # pragma: no cover
    raw_name = Column(String(32), nullable=False)
    hiragana = Column(String(32), nullable=False)
    english_id = Column(String(32), nullable=False)
    pronunciation = Column(String(32))
    other_names = Column(String(64))
    num_titles = Column(Integer)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'rawName': self.raw_name,
            'hiragana': self.hiragana,
            'englishId': self.english_id,
            'pronunciation': self.pronunciation,
        }
