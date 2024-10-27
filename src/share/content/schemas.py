from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class UniqueFieldsEnum(str, Enum):
    id = "id"
    slug = "slug"


class BasicBlogContent(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    slug: str = Field(max_length=150)

    short_description: str = Field(max_length=300)
    web_description: str = Field(max_length=300)
    og_description: str = Field(max_length=300)

    title: str = Field(max_length=100)
    web_title: str = Field(max_length=100)
    og_title: str = Field(max_length=100)

    content: str = Field()
    keywords: str = Field(max_length=150)

    is_published: bool = Field(False)
    reading_time: int = Field(gt=0, le=120)
    views_count: int = Field(ge=0)

    preview_file_id: Optional[UUID] = Field(None)
    preview_og_file_id: Optional[UUID] = Field(None)

    class Config:
        from_attributes = True


class GetBlogContent(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    slug: str = Field(max_length=150)

    short_description: str = Field(max_length=300)
    web_description: Optional[str] = Field(max_length=300)
    og_description: Optional[str] = Field(max_length=300)

    title: str = Field(max_length=100)
    web_title: Optional[str] = Field(max_length=100)
    og_title: Optional[str] = Field(max_length=100)

    keywords: Optional[str] = Field(max_length=150)

    is_published: bool = Field(False)
    reading_time: int = Field(gt=0, le=120)
    views_count: int = Field(ge=0)

    preview_file_id: Optional[UUID] = Field(None)
    preview_og_file_id: Optional[UUID] = Field(None)


class BasicEditableBlogContent(BaseModel):
    short_description: str = Field(max_length=300)
    web_description: str = Field(max_length=300)
    og_description: str = Field(max_length=300)

    title: str = Field(max_length=100)
    web_title: str = Field(max_length=100)
    og_title: str = Field(max_length=100)

    content: str = Field()
    keywords: str = Field(max_length=150)

    is_published: bool = Field(False)
    reading_time: int = Field(gt=0, le=120)
    views_count: int = Field(gt=0)

    preview_file_id: Optional[UUID] = Field(None)
    preview_og_file_id: Optional[UUID] = Field(None)

    class Config:
        from_attributes = True


class GetBlogContentResponse(BasicBlogContent):
    class Config:
        from_attributes = True


class CreateBlogContent(BasicEditableBlogContent):
    pass


class UpdateBlogContent(BaseModel):
    short_description: Optional[str] = Field(max_length=300)
    web_description: Optional[str] = Field(max_length=300)
    og_description: Optional[str] = Field(max_length=300)

    title: Optional[str] = Field(max_length=100)
    web_title: Optional[str] = Field(max_length=100)
    og_title: Optional[str] = Field(max_length=100)

    content: Optional[str] = Field()
    keywords: Optional[str] = Field(max_length=150)

    is_published: Optional[bool] = Field(False)
    reading_time: Optional[int] = Field(gt=0, le=120)
    views_count: Optional[int] = Field(gt=0)

    preview_file_id: Optional[UUID] = Field(None)
    preview_og_file_id: Optional[UUID] = Field(None)
