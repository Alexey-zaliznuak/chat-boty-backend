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

class BasicPost(BasicBlogContent):
    pass

class BasicEditablePost(BasicEditableBlogContent):
    pass

class GetPostResponse(GetBlogContent):
    class Config:
        from_attributes = True

class CreatePost(BasicEditablePost):
    pass

class UpdatePost(UpdateBlogContent):
    pass
