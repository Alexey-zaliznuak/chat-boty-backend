import os
from typing import override
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import delete, func, select, and_, true
from sqlalchemy.ext.asyncio import AsyncSession

from src.posts.schemas import UniqueFieldsEnum
from src.utils import SingletonMeta
from src.infrastructure.database import BaseORMService

from .config import PostsConfig
from .models import Post


class PostsService(BaseORMService, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__(
            base_model=Post
        )

    async def get_by_unique_field_or_404(self, identifier: str, field: UniqueFieldsEnum, session: AsyncSession) -> Post | None:
        result = await self.get_by_unique_field(identifier, field, session)

        if result is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")

        return result

    async def get_by_unique_field(self, identifier: str, field: UniqueFieldsEnum, session: AsyncSession) -> Post | None:
        unique_field = getattr(self.BASE_MODEL, field)

        query = await session.execute(select(self.BASE_MODEL).where(unique_field == identifier))

        result = query.fetchone()

        return result[0] if result is not None else None

    async def save_content_file(self, post_id: UUID, file: UploadFile) -> str:
        directory_path = os.path.join(PostsConfig.UPLOAD_DIRECTORY, post_id.hex)
        file_path = os.path.join(directory_path, f"{PostsConfig.POSTS_CONTENT_FILE_NAME}.{PostsConfig.POSTS_CONTENT_FILE_EXTENSION}")

        return await self._save_file(directory_path, file_path, file)

    async def save_preview_file(self, post_id: UUID, file: UploadFile) -> str:
        directory_path = os.path.join(PostsConfig.UPLOAD_DIRECTORY, post_id.hex)
        file_path = os.path.join(directory_path, f"{PostsConfig.POSTS_PREVIEW_FILE_NAME}.{PostsConfig.POSTS_PREVIEW_FILE_EXTENSION}")

        return await self._save_file(directory_path, file_path, file)

    async def _save_file(self, directory_path: str, file_path: str, file: UploadFile):
        os.makedirs(directory_path, exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path
