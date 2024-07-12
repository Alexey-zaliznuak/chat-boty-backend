from typing import Any
from uuid import UUID

from fastapi import Depends

from src.database import get_async_session

from .service import PostsService as Service


async def validate_post_id(id: UUID, session=Depends(get_async_session)) -> dict[str, Any]:
    return await Service().get_by_id(id, session)
