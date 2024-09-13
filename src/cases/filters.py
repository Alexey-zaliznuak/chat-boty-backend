from typing import Optional
from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import or_
from src.infrastructure.database.types import Where
from src.infrastructure.database.filtering import BaseFilterModel
from .models import Case


class CaseFilterParams(BaseModel, BaseFilterModel):
    has_content : Optional[bool] = Query(None)

    def to_where_statement(self) -> Where:
        return [
            self.to_where_has_content(),
        ]

    def to_where_has_content(self) -> Where:
        if self.has_content == True:
            return [
                Case.content.is_not(None),
            ]

        if self.has_content == False:
            return [
                Case.content_file.is_(None),
            ]
