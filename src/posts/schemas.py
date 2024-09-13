from enum import Enum
from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID

from src.infrastructure.database.types import Where
from src.infrastructure.database.filtering import BaseFilterModel

from .models import Post


class UniqueFieldsEnum(str, Enum):
    id = "id"
    slug = "slug"



class BasicPost(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    title: str = Field(max_length=100)
    slug: str = Field(max_length=150)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    content: str
    preview_file_id: str = Field(max_length=100)
    preview_og_file_id: str = Field(max_length=100)

    class Config:
        from_attributes = True


class BasicEditablePost(BaseModel):
    title: str = Field(max_length=100)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    content: str
    preview_file_id: str = Field(max_length=100)
    preview_og_file_id: str = Field(max_length=100)

    class Config:
        from_attributes = True


class GetPostResponse(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    title: str = Field(max_length=100)
    slug: str = Field(max_length=150)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    preview_file_id: str = Field(max_length=100)
    preview_og_file_id: str = Field(max_length=100)

    class Config:
        from_attributes = True


class CreatePost(BasicEditablePost):
    pass


class UpdatePost(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=150)
    short_description: Optional[str] = Field(None, max_length=300)
    reading_time: Optional[int] = Field(None, gt=0, le=120)

    content: str

    preview_file_id: Optional[str] = Field(None, max_length=100)
    preview_og_file_id: Optional[str] = Field(None, max_length=100)
