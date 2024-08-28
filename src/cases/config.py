import os
from src.config import BaseConfig


class CasesConfig(BaseConfig):
    UPLOAD_DIRECTORY = os.path.join(BaseConfig.ARTIFACT_DIRECTORY, "cases")

    CASES_CONTENT_FILE_NAME = "content"
    CASES_CONTENT_FILE_EXTENSION = "mdx"
    CASES_CONTENT_FILE_MEDIA_TYPE = "text/mdx"

    CASES_PREVIEW_FILE_NAME = "preview"
    CASES_PREVIEW_FILE_EXTENSION = "webp"
    CASES_PREVIEW_FILE_MEDIA_TYPE = "image/webp"
