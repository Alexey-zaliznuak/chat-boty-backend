from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from src.infrastructure.database.types import Where
from src.infrastructure.database.filtering import BaseFilterModel
from .models import Post


class PostFilterParams(BaseModel, BaseFilterModel):
    has_full_content: Optional[bool] = Query(None)
    is_published: Optional[bool] = Query(None)

    def to_where_statement(self) -> Where:
        return [
            self.to_where_has_full_content(),
            self.to_where_is_published(),
        ]

    def to_where_has_full_content(self) -> Where:
        if self.has_full_content == True:
            return [
                Post.content.is_not(None),
                Post.preview_file_id.is_not(None),
            ]

        if self.has_full_content == False:
            return or_(
                Post.content.is_(None),
                Post.preview_file_id.is_(None),
            )

    def to_where_is_published(self) -> Where:
        if self.is_published == True:
            return [
                Post.is_published == True,
            ]

        if self.is_published == False:
            return or_(
                Post.is_published == False,
            )
