from logging.config import fileConfig

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool

from alembic import context

from src.config import Config
from src.posts.models import Base as PostsBase


config = context.config

section = config.config_ini_section
config.set_section_option(section, "DATABASE_URL", Config.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


target_metadata = [PostsBase.metadata]


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        future=True,
        echo=True,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        async with connection.begin():
            connection.run_sync(context.run_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    asyncio.run(run_migrations_online())
