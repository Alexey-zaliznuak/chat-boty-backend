from enum import Enum

from src.share.content.schemas import (
    BasicBlogContent,
    BasicEditableBlogContent,
    GetBlogContent,
    UpdateBlogContent
)

class UniqueFieldsEnum(str, Enum):
    id = "id"
    slug = "slug"

class BasicCase(BasicBlogContent):
    pass

class BasicEditableCase(BasicEditableBlogContent):
    pass

class GetCaseResponse(GetBlogContent):
    class Config:
        from_attributes = True

class CreateCase(BasicEditableCase):
    pass

class UpdateCase(UpdateBlogContent):
    pass
