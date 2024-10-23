from src.share.content.schemas import BasicBlogContent, BasicEditableBlogContent, UpdateBlogContent

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
