from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


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

    is_published: bool = Field(False)

    content: str
    preview_file_id: UUID = Field()
    preview_og_file_id: UUID = Field()

    class Config:
        from_attributes = True


class BasicEditablePost(BaseModel):
    title: str = Field(max_length=100)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    is_published: bool = Field(False)

    content: str = Field(max_length=30_000)

    preview_file_id: Optional[UUID] = Field(None)
    preview_og_file_id: Optional[UUID] = Field(None)

    class Config:
        from_attributes = True


class GetPostResponse(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    is_published: bool = Field(False)

    title: str = Field(max_length=100)
    slug: str = Field(max_length=150)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    preview_file_id: Optional[UUID] = Field()
    preview_og_file_id: Optional[UUID] = Field()

    class Config:
        from_attributes = True


class CreatePost(BasicEditablePost):
    pass


class UpdatePost(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=150)
    short_description: Optional[str] = Field(None, max_length=300)
    reading_time: Optional[int] = Field(None, gt=0, le=120)

    is_published: Optional[bool] = Field(None)

    content: Optional[str] = Field(None, max_length=30_000)

    preview_file_id: Optional[UUID] = Field(None)
    preview_og_file_id: Optional[UUID] = Field(None)
