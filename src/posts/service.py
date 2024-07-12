import os
from typing import override
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.utils.singleton import SingletonMeta
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

    async def save_file(self, post_id: UUID, file: UploadFile):
        directory_path = os.path.join(PostsConfig.UPLOAD_DIRECTORY, post_id.hex)
        file_path = os.path.join(directory_path, f"{PostsConfig.POSTS_FILE_NAME}.{PostsConfig.POSTS_FILE_EXTENSION}")

        os.makedirs(directory_path, exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path

    async def _delete_file(self, file: str):
        os.remove(file)
