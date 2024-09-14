from typing import Any
from uuid import UUID

from fastapi import Depends, HTTPException, Query, Request
from pydantic import UUID4

from src.utils import is_uuid
from .schemas import UniqueFieldsEnum
from .filters import PostFilterParams

from src.database import get_async_session

from .service import PostsService as Service


async def validate_post(
    identifier: str,
    field: UniqueFieldsEnum = Query(UniqueFieldsEnum.slug),
    session=Depends(get_async_session)
) -> dict[str, Any]:
    field = UniqueFieldsEnum.slug if field is None else field

    if field == UniqueFieldsEnum.id and not is_uuid(identifier):
        raise HTTPException(status_code=400, detail="Invalid UUID identifier.")

    return await Service().get_by_unique_field_or_404(identifier, field, session)

async def validate_post_slug(post_slug: str, session=Depends(get_async_session)) -> dict[str, Any]:
    return await Service().get_by_slug(post_slug, session)

async def validate_post_id(post_id: UUID, session=Depends(get_async_session)) -> dict[str, Any]:
    return await Service().get_by_id(post_id, session)

def get_post_filter_params(
    hasFullContent: bool | None = Query(None),
    isPublished: bool | None = Query(None),
) -> PostFilterParams:
    return PostFilterParams(has_full_content=hasFullContent, is_published=isPublished)
