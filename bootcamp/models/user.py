import uuid

from bootcamp.models.base import Model
from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import UUID


class User(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID, default=lambda: str(uuid.uuid4()), nullable=False)  # pragma: no cover
    user_name = Column(String(20), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(320))

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'id': self.id,
            'userName': self.user_name,
            'password': self.password,
            'email': self.email,
        }
