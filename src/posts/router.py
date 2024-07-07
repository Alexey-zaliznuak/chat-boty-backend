from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from .models import Post
from .schemas import PostResponse
from .service import PostsService


router = APIRouter(prefix="/posts", tags=["posts"])


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
