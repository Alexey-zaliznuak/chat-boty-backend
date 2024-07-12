import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    title = Column(String(100), nullable=False)
    short_description = Column(String(300), nullable=False)
    reading_time = Column(Integer, CheckConstraint('reading_time > 0 AND reading_time <= 120'), nullable=False)

    file = Column(String, nullable=True)

    @staticmethod
    def validate_reading_time(mapper, connection, target):
        if target.reading_time <= 0 or target.reading_time > 120:
            raise ValueError("reading_time must be between 1 and 120")

event.listen(Post, 'before_insert', Post.validate_reading_time)
event.listen(Post, 'before_update', Post.validate_reading_time)
