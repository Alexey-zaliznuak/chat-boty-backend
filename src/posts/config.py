import os
from src.config import BaseConfig


class PostsConfig(BaseConfig):
    UPLOAD_DIRECTORY = os.path.join(BaseConfig.ARTIFACT_DIRECTORY, "posts")

    POSTS_CONTENT_FILE_NAME = "content"
    POSTS_CONTENT_FILE_EXTENSION = "md"
    POSTS_CONTENT_FILE_MEDIA_TYPE = "text/markdown"

    POSTS_PREVIEW_FILE_NAME = "preview"
    POSTS_PREVIEW_FILE_EXTENSION = "webp"
    POSTS_PREVIEW_FILE_MEDIA_TYPE = "image/webp"
