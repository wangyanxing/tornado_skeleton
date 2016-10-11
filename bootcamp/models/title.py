import uuid

from bootcamp.lib.validation import is_valid_uuid_string
from bootcamp.models import logger
from bootcamp.models.base import Model
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID


class Title(Model):
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID, default=lambda: str(uuid.uuid4()), nullable=False)  # pragma: no cover
    title_id = Column(String(10), nullable=False)
    title = Column(Text, nullable=False)
    video_path = Column(String(128), nullable=False)
    file_names = Column(String(128), nullable=False)
    description = Column(Text)
    video_size = Column(Integer)  # In bytes
    rate = Column(Integer)

    @classmethod
    def get(cls, uuid):
        logger.info("Accessed title {} with UUID".format(uuid))
        q = cls.query().filter_by(uuid=is_valid_uuid_string(uuid))
        return q.first()

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'id': self.id,
            'titleId': self.title_id,
            'title': self.title,
            'videoPath': self.video_path,
            'fileNames': self.file_names,
            'description': self.description,
            'videoSize': self.video_size,
            'rate': self.rate,
        }
