import os
from typing import Literal
from uuid import UUID

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
from .dependencies import validate_post, validate_post_id, get_post_filter_params, validate_post_slug
from .models import Post
from .schemas import (
    BasicPost,
    CreatePost,
    GetPostResponse,
    PostFilterParams,
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

    @router.get("/{identifier}/files/content")
    @limiter.limit("10/minute")
    async def get_content_file(
        self,
        request: Request,
        post: Post = Depends(validate_post)
    ):
        if post.content_file is None or not os.path.exists(post.content_file):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(path=post.content_file, media_type=Config.POSTS_CONTENT_FILE_MEDIA_TYPE)

    @router.get("/{identifier}/files/preview")
    @limiter.limit("10/minute")
    async def get_preview_file(
        self,
        request: Request,
        post: Post = Depends(validate_post)
    ):
        if post.preview_file is None or not os.path.exists(post.preview_file):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(path=post.preview_file, media_type=Config.POSTS_CONTENT_FILE_MEDIA_TYPE)

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

    @router.put("/{identifier}/files/content", response_model=GetPostResponse)
    @admin_access()
    async def upload_content_file(
        self,
        request: Request,
        file: UploadFile = File(...),
        post: Post = Depends(validate_post)
    ):
        await self.service.update_instance_fields(
            post,
            data={"content_file": await self.service.save_content_file(post.id, file)},
            session=self.session,
            save=True,
        )
        return post

    @router.put("/{identifier}/files/preview", response_model=GetPostResponse)
    @admin_access()
    async def upload_preview_file(
        self,
        request: Request,
        file: UploadFile = File(...),
        post: Post = Depends(validate_post)
    ):
        await self.service.update_instance_fields(
            post,
            data={"preview_file": await self.service.save_preview_file(post.id, file)},
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
            await self.service.delete_by_id(post.id, post.file, self.session)

        except FileNotFoundError:
            print("FILE NOT FOUND", post.file, flush=True)
            raise

        return Response(status_code=status.HTTP_204_NO_CONTENT)
