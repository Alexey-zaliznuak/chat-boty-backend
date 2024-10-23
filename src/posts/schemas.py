from enum import Enum

from src.share.content.schemas import (
    BasicBlogContent,
    BasicEditableBlogContent,
    UpdateBlogContent
)

class UniqueFieldsEnum(str, Enum):
    id = "id"
    slug = "slug"

class BasicPost(BasicBlogContent):
    pass

class BasicEditablePost(BasicEditableBlogContent):
    pass

class GetPostResponse(BasicPost):
    class Config:
        from_attributes = True

class CreatePost(BasicEditablePost):
    pass

class UpdatePost(UpdateBlogContent):
    pass
