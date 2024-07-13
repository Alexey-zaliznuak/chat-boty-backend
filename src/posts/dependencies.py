from typing import Any
from uuid import UUID

from fastapi import Depends, Query, Request
from .schemas import PostFilterParams

from src.database import get_async_session

from .service import PostsService as Service


async def validate_post_id(id: UUID, session=Depends(get_async_session)) -> dict[str, Any]:
    return await Service().get_by_id(id, session)

def get_post_filter_params(has_file: bool | None = Query(None)) -> PostFilterParams:
    return PostFilterParams(has_file=has_file)
