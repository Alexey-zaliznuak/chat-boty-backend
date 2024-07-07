import os
from uuid import UUID
from fastapi import UploadFile
from .config import PostsConfig


class PostsService:
    @staticmethod
    async def save_file(post_id: UUID, file: UploadFile):
        directory_path = os.path.join(PostsConfig.UPLOAD_DIRECTORY,post_id.hex,)
        file_path = os.path.join(directory_path, f"{PostsConfig.POSTS_FILE_NAME}.{PostsConfig.POSTS_FILE_EXTENSION}")

        os.makedirs(directory_path, exist_ok=True)

        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        return file_path
