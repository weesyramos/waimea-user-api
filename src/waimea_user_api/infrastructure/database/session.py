from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from waimea_user_api.config import settings


DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}"
    f"/{settings.database_name}"
)

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session():
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise