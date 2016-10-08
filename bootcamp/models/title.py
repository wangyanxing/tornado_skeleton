import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    Unicode,
)
from sqlalchemy.dialects.postgresql import UUID

from bootcamp.lib.validation import is_valid_uuid_string
from bootcamp.models import Model, logger


class Title(Model):
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, default=lambda: str(uuid.uuid4()))
    title_id = Column(String(10))
    title = Column(Text)
    video_path = Column(String(128))
    file_names = Column(String(128))
    description = Column(Text)
    video_size = Column(Integer)  # In bytes
    rate = Column(Integer)

    @classmethod
    def get(cls, uuid):
        logger.info("Accessed title {} with UUID".format(uuid))
        q = cls.query().filter_by(uuid=is_valid_uuid_string(uuid))
        return q.first()

    def to_dict(self):
        """Return a dictionary representation of the model."""
        return {
            'uuid': self.uuid,
            'id': self.uuid,
            'titleId': self.title_id,
            'title': self.title,
            'videoPath': self.video_path,
            'fileNames': self.file_names,
            'description': self.description,
            'videoSize': self.video_size,
            'rate': self.rate,
        }
