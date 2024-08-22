import os
from typing import override
from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import delete, func, select, and_, true
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils import SingletonMeta
from src.infrastructure.database import BaseORMService

from .config import PostsConfig
from .models import Post


class PostsService(BaseORMService, metaclass=SingletonMeta):
    def __init__(self):
        super().__init__(
            base_model=Post
        )

    @override
    async def delete_by_id(self, post_id: UUID, post_file: str, session: AsyncSession):
        await super().delete_by_id(post_id, session)

        if post_file:
            await self._delete_file(post_file)

    async def get_by_slug(self, slug: str, session: AsyncSession, *, throw_not_found: bool = True):
        query = await session.execute(select(self.BASE_MODEL).where(self.BASE_MODEL.slug == slug))
        result = query.fetchone()

        if result is None:
            if throw_not_found:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
            return None

        obj = result[0]
        return obj

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

    async def _delete_file(self, file: str):
        os.remove(file)
