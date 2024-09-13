from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from src.infrastructure.database.types import Where
from src.infrastructure.database.filtering import BaseFilterModel
from .models import Post


class PostFilterParams(BaseModel, BaseFilterModel):
    has_full_content: Optional[bool] = Query(None)

    def to_where_statement(self) -> Where:
        return [
            self.to_where_has_full_content(),
            self.to_where_preview_file_id(),
        ]

    def to_where_has_full_content(self) -> Where:
        if self.has_full_content == True:
            return Post.content.is_not(None)

        if self.has_full_content == False:
            return Post.content.is_(None)

    # def to_where_search(self) -> Where:
    #     if self.search:
    #         return or_(
    #             Post.title.ilike(self.search),
    #             Post.content.ilike(self.search)
    #         )
