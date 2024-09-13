from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class UniqueFieldsEnum(str, Enum):
    id = "id"
    slug = "slug"


class BasicCase(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    title: str = Field(max_length=100)
    slug: str = Field(max_length=150)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    content: str = Field(max_length=300)
    preview_file_id: str = Field(max_length=100)
    preview_og_file_id: str = Field(max_length=100)

    class Config:
        from_attributes = True


class BasicEditableCase(BaseModel):
    title: str = Field(max_length=100)
    short_description: str = Field(max_length=300)
    reading_time: int = Field(gt=0, le=120)

    content: str
    preview_file_id: str = Field(max_length=100)
    preview_og_file_id: str = Field(max_length=100)

    class Config:
        from_attributes = True


class GetCaseResponse(BaseModel):
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


class CreateCase(BasicEditableCase):
    pass


class UpdateCase(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    slug: Optional[str] = Field(None, max_length=150)
    short_description: Optional[str] = Field(None, max_length=300)
    reading_time: Optional[int] = Field(None, gt=0, le=120)
    content: Optional[str] = Field(None)

    preview_file_id: str = Field(max_length=100)
    preview_og_file_id: str = Field(max_length=100)
