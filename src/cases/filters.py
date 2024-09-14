from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from src.infrastructure.database.types import Where
from src.infrastructure.database.filtering import BaseFilterModel
from .models import Case


class CaseFilterParams(BaseModel, BaseFilterModel):
    has_full_content : Optional[bool] = Query(None)
    is_published : Optional[bool] = Query(None)

    def to_where_statement(self) -> Where:
        return [
            self.to_where_has_content(),
        ]

    def to_where_has_content(self) -> Where:
        if self.has_full_content == True:
            return [
                Case.content.is_not(None),
                Case.preview_file_id.is_not(None),
            ]

        if self.has_full_content == False:
            return or_(
                Case.content.is_(None),
                Case.preview_file_id.is_(None),
            )

    def to_where_is_published(self) -> Where:
        if self.is_published == True:
            return [
                Case.is_published == True,
            ]

        if self.has_full_content == False:
            return or_(
                Case.is_published == False,
            )
