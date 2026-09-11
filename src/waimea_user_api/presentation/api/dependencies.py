from collections.abc import AsyncGenerator

from fastapi import Depends
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from waimea_user_api.application.use_cases.create_user import CreateUserUseCase
from waimea_user_api.domain.repositories.user_repository import UserRepository
from waimea_user_api.infrastructure.database.session import async_session
from waimea_user_api.infrastructure.repositories.sqlalchemy_user_repository import (
    SqlAlchemyUserRepository,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def get_password_hasher() -> PasswordHash:
    return PasswordHash.recommended()


def get_create_user_use_case(
    user_repository: UserRepository = Depends(get_user_repository),
    password_hasher: PasswordHash = Depends(get_password_hasher),
) -> CreateUserUseCase:
    return CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )