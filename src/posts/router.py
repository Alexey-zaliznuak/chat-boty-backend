from uuid import UUID, uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import func, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.pagination import PaginatedResponse, PaginationParams, get_pagination_params

from src.database import get_async_session

from .models import Post
from .schemas import PostResponse
from .service import PostsService


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post_id: UUID, session: AsyncSession = Depends(get_async_session)):
    query = await session.execute(select(Post).where(Post.id == post_id))
    await session.commit()

    post = query.fetchone()[0]

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return post

@router.get("/", response_model=PaginatedResponse[PostResponse])
async def get_all_posts(
    session: AsyncSession = Depends(get_async_session),
    pagination: PaginationParams = Depends(get_pagination_params),
):
    query = pagination.apply_pagination(
        select(
            Post,
            func.count(Post.id).over().label("total_items")
        ).order_by(
            Post.created_at.desc()
        )
    )

    result = await session.execute(query)
    rows = result.fetchall()

    posts, total_items = zip(*rows) if rows else ([], [0])

    return PaginatedResponse(
        data=posts,
        pagination=pagination,
        total_items=total_items[0]
    )

@router.post("/", response_model=PostResponse)
async def create_post(file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    post_id = uuid4()

    file_path = await PostsService.save_file(post_id, file)

    query = await session.execute(insert(Post).values(id=post_id, file=file_path).returning(Post))
    await session.commit()

    created_post = query.fetchone()[0]

    if not created_post:
        raise HTTPException(409, "Failed to create post")

    return created_post
