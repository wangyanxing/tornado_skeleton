import uuid

from bootcamp.models.base import Model
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID


class Title(Model):
    __tablename__ = 'titles'

    id = Column(Integer, primary_key=True, nullable=False)
    uuid = Column(UUID, default=lambda: str(uuid.uuid4()), nullable=False)  # pragma: no cover
    title_id = Column(String(10), nullable=False)
    title = Column(Text, nullable=False)
    video_path = Column(String(128), nullable=False)
    file_names = Column(String(128), nullable=False)
    description = Column(Text)
    maker = Column(String(32))
    video_size = Column(Integer)  # In bytes
    stars = Column(Integer)
    rate = Column(Numeric)
    length = Column(Integer)
    published_date = Column(DateTime)
    tags = Column(ARRAY(Integer))

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
            'length': self.length,
            'publishedDate': str(self.published_date),
        }
