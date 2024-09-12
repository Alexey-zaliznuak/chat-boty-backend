import os

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Query,
    Request,
    Response,
    UploadFile,
    status
)
from fastapi.responses import FileResponse
from fastapi_restful.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.auth import admin_access
from src.database import get_async_session
from src.infrastructure.route.pagination import (
    PaginatedResponse,
    PaginationParams,
    get_pagination_params
)
from src.infrastructure.rate_limit import limiter

from .config import PostsConfig as Config
from .dependencies import validate_post, get_post_filter_params
from .models import Post
from .filters import PostFilterParams
from .schemas import (
    BasicPost,
    CreatePost,
    GetPostResponse,
    UniqueFieldsEnum,
    UpdatePost,
)
from .service import PostsService


router = APIRouter(prefix="/posts", tags=["posts"])


@cbv(router)
class PostsView:
    service = PostsService()
    session: AsyncSession = Depends(get_async_session)

    @router.get("/", response_model=PaginatedResponse[GetPostResponse])
    @limiter.limit("10/minute")
    async def get_all(
        self,
        request: Request,
        pagination: PaginationParams = Depends(get_pagination_params),
        filters: PostFilterParams = Depends(get_post_filter_params)
    ):
        return await self.service.get_many_with_pagination(
            pagination,
            self.session,
            where=filters,
        )

    @router.get("/{identifier}/", response_model=GetPostResponse)
    @limiter.limit("10/minute")
    async def get(
        self,
        request: Request,
        post: Post = Depends(validate_post)
    ):
        return post

    @router.get("/{identifier}/content")
    @limiter.limit("10/minute")
    async def get_content(
        self,
        request: Request,
        post: Post = Depends(validate_post)
    ) -> str:
        return post.content

    @router.post("/", response_model=GetPostResponse)
    @admin_access()
    async def create(self, data: CreatePost, request: Request):
        new_post = Post(
            title=data.title,
            slug=await Post.generate_slug(data.title, self.session),
            short_description=data.short_description,
            reading_time=data.reading_time,
        )

        await self.service.save_and_refresh(new_post, self.session)

        if not new_post:
            raise HTTPException(status.HTTP_409_CONFLICT, "Failed to create post")

        return new_post

    @router.patch("/{identifier}", response_model=GetPostResponse)
    @admin_access()
    async def update(
        self,
        data: UpdatePost,
        request: Request,
        post: Post = Depends(validate_post)
    ):
        await self.service.update_instance_fields(
            post,
            data=data.model_dump(exclude_unset=True),
            session=self.session,
            save=True,
        )
        return post

    @router.delete("/{identifier}", response_model=None)
    @admin_access()
    async def delete(
        self,
        request: Request,
        post: Post = Depends(validate_post),
    ):
        try:
            await self.service.delete_by_id(post.id, self.session)

        except FileNotFoundError:
            print("FILE NOT FOUND", post.file, flush=True)
            raise

        return Response(status_code=status.HTTP_204_NO_CONTENT)
