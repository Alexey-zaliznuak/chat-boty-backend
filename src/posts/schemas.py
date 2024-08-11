from enum import Enum
from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from uuid import UUID

from src.infrastructure.database.types import Where
from src.infrastructure.database.filtering import BaseFilterModel

from .models import Post


class BasicPost(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    title: str = Field(max_length=100)
    slug: str = Field(max_length=150)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    content_file: str
    preview_file: str

    class Config:
        from_attributes = True


class UniqueFieldsEnum(str, Enum):
    id = "id"
    slug = "slug"


class BasicEditablePost(BaseModel):
    title: str = Field(max_length=100)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

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

    class Config:
        from_attributes = True


class PostFilterParams(BaseModel, BaseFilterModel):
    has_file: Optional[bool] = Query(None)

    def to_where_statement(self) -> Where:
        return [
            self.to_where_has_file(),
        ]

    def to_where_has_file(self) -> Where:
        if self.has_file == False:
            return Post.file.is_(None)

        if self.has_file == True:
            return Post.file.is_not(None)

        return None


class CreatePost(BasicEditablePost):
    pass


class UpdatePost(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=150)
    short_description: Optional[str] = Field(None, max_length=300)
    reading_time: Optional[int] = Field(None, gt=0, le=120)
