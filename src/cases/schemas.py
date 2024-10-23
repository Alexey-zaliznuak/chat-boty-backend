from enum import Enum

from src.share.content.schemas import (
    BasicBlogContent,
    BasicEditableBlogContent,
    UpdateBlogContent
)

class UniqueFieldsEnum(str, Enum):
    id = "id"
    slug = "slug"

class BasicCase(BasicBlogContent):
    pass

class BasicEditableCase(BasicEditableBlogContent):
    pass

class GetCaseResponse(BasicCase):
    class Config:
        from_attributes = True

class CreateCase(BasicEditableCase):
    pass

class UpdateCase(UpdateBlogContent):
    pass
