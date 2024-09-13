from typing import Any

from fastapi import Depends, HTTPException, Query

from src.utils import is_uuid
from .schemas import UniqueFieldsEnum
from .filters import CaseFilterParams

from src.database import get_async_session

from .service import CasesService as Service


async def validate_case(
    identifier: str,
    field: UniqueFieldsEnum = Query(UniqueFieldsEnum.slug),
    session=Depends(get_async_session)
) -> dict[str, Any]:
    field = UniqueFieldsEnum.slug if field is None else field

    if field == UniqueFieldsEnum.id and not is_uuid(identifier):
        raise HTTPException(status_code=400, detail="Invalid UUID identifier.")

    return await Service().get_by_unique_field_or_404(identifier, field, session)

def get_cases_filter_params(hasFullContent: bool | None = Query(None)) -> CaseFilterParams:
    return CaseFilterParams(hasFullContent=hasFullContent)
