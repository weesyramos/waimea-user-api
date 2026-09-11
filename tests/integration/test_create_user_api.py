from uuid import uuid4

import httpx
import pytest
from pwdlib import PasswordHash
from sqlalchemy import delete, select

from waimea_user_api.infrastructure.database.models.role import Role
from waimea_user_api.infrastructure.database.models.user import User
from waimea_user_api.infrastructure.database.session import async_session
from waimea_user_api.main import app


@pytest.mark.asyncio
async def test_create_user_with_generated_password():
    # Cria uma role exclusiva para este teste.
    role_description = f"test-{uuid4()}"

    async with async_session() as session:
        role = Role(description=role_description)
        session.add(role)

        await session.commit()
        await session.refresh(role)

        role_id = role.id

    email = f"test-{uuid4()}@example.com"

    try:
        # Usa um cliente HTTP assíncrono no mesmo event loop do teste.
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/users",
                json={
                    "name": "Integration Test",
                    "email": email,
                    "role_id": role_id,
                },
            )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["name"] == "Integration Test"
        assert response_data["email"] == email
        assert response_data["role_id"] == role_id
        assert response_data["generated_password"] is not None

        generated_password = response_data["generated_password"]

        # Confirma que o usuário foi realmente persistido.
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))

            user = result.scalar_one()

            assert user.name == "Integration Test"
            assert user.role_id == role_id
            assert user.password != generated_password

            # Confirma que a senha retornada corresponde ao hash armazenado.
            password_hasher = PasswordHash.recommended()

            assert password_hasher.verify(
                generated_password,
                user.password,
            )

    finally:
        # Remove os dados criados pelo teste.
        async with async_session() as session:
            await session.execute(delete(User).where(User.email == email))

            await session.execute(delete(Role).where(Role.id == role_id))

            await session.commit()


@pytest.mark.asyncio
async def test_create_user_with_provided_password():
    role_description = f"test-{uuid4()}"

    async with async_session() as session:
        role = Role(description=role_description)
        session.add(role)

        await session.commit()
        await session.refresh(role)

        role_id = role.id

    email = f"test-{uuid4()}@example.com"
    password = "my-secure-password"

    try:
        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/users",
                json={
                    "name": "Integration Test",
                    "email": email,
                    "role_id": role_id,
                    "password": password,
                },
            )

        assert response.status_code == 201

        response_data = response.json()

        assert response_data["name"] == "Integration Test"
        assert response_data["email"] == email
        assert response_data["role_id"] == role_id
        assert response_data["generated_password"] is None

        async with async_session() as session:
            result = await session.execute(select(User).where(User.email == email))

            user = result.scalar_one()

            password_hasher = PasswordHash.recommended()

            assert password_hasher.verify(
                password,
                user.password,
            )

    finally:
        async with async_session() as session:
            await session.execute(delete(User).where(User.email == email))

            await session.execute(delete(Role).where(Role.id == role_id))

            await session.commit()
