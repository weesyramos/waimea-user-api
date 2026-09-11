from unittest.mock import AsyncMock, Mock

import pytest
from pwdlib import PasswordHash

from waimea_user_api.application.use_cases.create_user import (
    CreateUserData,
    CreateUserUseCase,
)
from waimea_user_api.application.exceptions import UserAlreadyExistsError
from waimea_user_api.domain.entities.user import User


@pytest.mark.asyncio
async def test_create_user_with_provided_password():
    # Mock do repository: não vamos acessar o banco neste teste.
    user_repository = Mock()
    user_repository.find_by_email = AsyncMock(return_value=None)
    user_repository.create = AsyncMock(
        return_value=User(
            id=1,
            name="John Doe",
            email="john@example.com",
            password="hashed-password",
            role_id=1,
        )
    )

    # Mock da transação.
    unit_of_work = Mock()
    unit_of_work.commit = AsyncMock()
    unit_of_work.rollback = AsyncMock()

    password_hasher = PasswordHash.recommended()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        unit_of_work=unit_of_work,
    )

    data = CreateUserData(
        name="John Doe",
        email="john@example.com",
        role_id=1,
        password="my-secret-password",
    )

    result = await use_case.execute(data)

    assert result.user.id == 1
    assert result.user.name == "John Doe"
    assert result.user.email == "john@example.com"
    assert result.generated_password is None

    user_repository.find_by_email.assert_awaited_once_with("john@example.com")
    user_repository.create.assert_awaited_once()

    unit_of_work.commit.assert_awaited_once()
    unit_of_work.rollback.assert_not_awaited()
    
@pytest.mark.asyncio
async def test_create_user_without_password_generates_password():
    user_repository = Mock()
    user_repository.find_by_email = AsyncMock(return_value=None)
    user_repository.create = AsyncMock(
        side_effect=lambda user: User(
            id=1,
            name=user.name,
            email=user.email,
            password=user.password,
            role_id=user.role_id,
            created_at=user.created_at,
        )
    )

    unit_of_work = Mock()
    unit_of_work.commit = AsyncMock()
    unit_of_work.rollback = AsyncMock()

    password_hasher = PasswordHash.recommended()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        unit_of_work=unit_of_work,
    )

    data = CreateUserData(
        name="John Doe",
        email="john@example.com",
        role_id=1,
    )

    result = await use_case.execute(data)

    assert result.user.id == 1
    assert result.generated_password is not None
    assert len(result.generated_password) > 0

    created_user = user_repository.create.await_args.args[0]

    assert created_user.password != result.generated_password
    assert password_hasher.verify(
        result.generated_password,
        created_user.password,
    )

    unit_of_work.commit.assert_awaited_once()
    unit_of_work.rollback.assert_not_awaited()
    
@pytest.mark.asyncio
async def test_create_user_with_existing_email():
    user_repository = Mock()
    user_repository.find_by_email = AsyncMock(
        return_value=User(
            id=1,
            name="John Doe",
            email="john@example.com",
            password="hashed-password",
            role_id=1,
        )
    )
    user_repository.create = AsyncMock()

    unit_of_work = Mock()
    unit_of_work.commit = AsyncMock()
    unit_of_work.rollback = AsyncMock()

    password_hasher = PasswordHash.recommended()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        unit_of_work=unit_of_work,
    )

    data = CreateUserData(
        name="Jane Doe",
        email="john@example.com",
        role_id=1,
        password="my-secret-password",
    )

    with pytest.raises(UserAlreadyExistsError):
        await use_case.execute(data)

    user_repository.create.assert_not_awaited()
    unit_of_work.commit.assert_not_awaited()
    unit_of_work.rollback.assert_awaited_once()
    
@pytest.mark.asyncio
async def test_create_user_rolls_back_when_repository_fails():
    user_repository = Mock()
    user_repository.find_by_email = AsyncMock(return_value=None)
    user_repository.create = AsyncMock(
        side_effect=RuntimeError("Database error")
    )

    unit_of_work = Mock()
    unit_of_work.commit = AsyncMock()
    unit_of_work.rollback = AsyncMock()

    password_hasher = PasswordHash.recommended()

    use_case = CreateUserUseCase(
        user_repository=user_repository,
        password_hasher=password_hasher,
        unit_of_work=unit_of_work,
    )

    data = CreateUserData(
        name="John Doe",
        email="john@example.com",
        role_id=1,
        password="my-secret-password",
    )

    with pytest.raises(RuntimeError, match="Database error"):
        await use_case.execute(data)

    unit_of_work.commit.assert_not_awaited()
    unit_of_work.rollback.assert_awaited_once()