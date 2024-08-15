from typing import Any
from uuid import UUID

from fastapi import Depends, Query, Request
from .schemas import PostFilterParams

from src.database import get_async_session

from .service import PostsService as Service


async def validate_post_id(post_id: UUID, session=Depends(get_async_session)) -> dict[str, Any]:
    return await Service().get_by_id(post_id, session)

async def validate_post_slug(post_slug: str, session=Depends(get_async_session)) -> dict[str, Any]:
    return await Service().get_by_slug(post_slug, session)

def get_post_filter_params(hasFullContent: bool | None = Query(None)) -> PostFilterParams:
    return PostFilterParams(hasFullContent=hasFullContent)
