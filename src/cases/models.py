import uuid
from datetime import datetime
from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Text, event, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils import slugify


Base = declarative_base()


class Case(Base):
    __tablename__ = 'cases'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    title = Column(String(100), nullable=False)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    short_description = Column(String(300), nullable=False)

    reading_time = Column(Integer, CheckConstraint('reading_time > 0 AND reading_time <= 120'), nullable=False)

    content = Column(Text, nullable=True)
    preview_file_id = Column(String(100), nullable=True)
    preview_og_file_id = Column(String(100), nullable=True)

    @staticmethod
    async def generate_slug(title: str, session: AsyncSession):
        base_slug = slugify(title)
        unique_slug = base_slug
        counter = 1

        while (
            await session.execute(select(Case).where(Case.slug == unique_slug))
        ).fetchone() is not None:
            unique_slug = f"{base_slug}-{counter}"
            counter += 1

        return unique_slug

    @staticmethod
    def validate_reading_time(mapper, connection, target):
        if target.reading_time <= 0 or target.reading_time > 120:
            raise ValueError("reading_time must be between 1 and 120")


event.listen(Case, 'before_insert', Case.validate_reading_time)
event.listen(Case, 'before_update', Case.validate_reading_time)
