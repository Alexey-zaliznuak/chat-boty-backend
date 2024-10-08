import contextlib
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import Config


Base = declarative_base()

engine = create_async_engine(Config.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


@contextlib.asynccontextmanager
async def get_async_session_with_context_manager() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
