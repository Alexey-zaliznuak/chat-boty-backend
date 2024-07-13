import os

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    Header,
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
from .dependencies import validate_post_id, get_post_filter_params
from .models import Post
from .schemas import (
    BasicPost,
    CreatePost,
    GetPostResponse,
    PostFilterParams,
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
    async def get_all_posts(
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


    @router.get("/{post_id}", response_model=GetPostResponse)
    @limiter.limit("10/minute")
    async def get_post_by_id(
        self,
        request: Request,
        post: BasicPost = Depends(validate_post_id),
    ):
        return post


    @router.get("/{post_id}/file")
    @limiter.limit("10/minute")
    async def download_post_file(
        self,
        request: Request,
        post: BasicPost = Depends(validate_post_id),
    ):
        if post.file is None or not os.path.exists(post.file):
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(path=post.file, media_type=Config.POSTS_FILE_MEDIA_TYPE)


    @router.post("/", response_model=GetPostResponse)
    @admin_access()
    async def create_post(self, data: CreatePost, request: Request):
        new_post = Post(
            title=data.title,
            short_description=data.short_description,
            reading_time=data.reading_time,
        )

        await self.service.save_and_refresh(new_post, self.session)

        if not new_post:
            raise HTTPException(status.HTTP_409_CONFLICT, "Failed to create post")

        return new_post


    @router.patch("/{post_id}", response_model=GetPostResponse)
    @admin_access()
    async def update_by_id(
        self,
        data: UpdatePost,
        request: Request,
        post: Post = Depends(validate_post_id),
    ):
        await self.service.update_instance_fields(
            post,
            data=data.model_dump(exclude_unset=True),
            session=self.session,
            save=True,
        )
        return post


    @router.put("/{post_id}/file", response_model=GetPostResponse)
    @admin_access()
    async def upload_post_file(
        self,
        request: Request,
        file: UploadFile = File(...),
        post: Post = Depends(validate_post_id),
    ):
        await self.service.update_instance_fields(
            post,
            data={"file": await self.service.save_file(post.id, file)},
            session=self.session,
            save=True,
        )
        return post


    @router.delete("/{post_id}", response_model=GetPostResponse)
    @admin_access()
    async def delete_post_by_id(
        self,
        request: Request,
        post: BasicPost = Depends(validate_post_id),
    ):
        try:
            await self.service.delete_by_id(post.id, post.file, self.session)

        except FileNotFoundError:
            print("FILE NOT FOUND", post.file, flush=True)

        return Response(status_code=status.HTTP_204_NO_CONTENT)
