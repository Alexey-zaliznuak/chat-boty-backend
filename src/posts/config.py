import os
from src.config import BaseConfig


class PostsConfig(BaseConfig):
    UPLOAD_DIRECTORY = os.path.join(BaseConfig.ARTIFACT_DIRECTORY, "posts")

    POSTS_FILE_NAME = "content"
    POSTS_FILE_EXTENSION = "html"
