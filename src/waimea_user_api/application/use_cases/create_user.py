import secrets
from dataclasses import dataclass
from datetime import date

from pwdlib import PasswordHash

from waimea_user_api.domain.entities.user import User
from waimea_user_api.domain.repositories.user_repository import UserRepository
from waimea_user_api.application.exceptions import UserAlreadyExistsError


@dataclass
class CreateUserData:
    name: str
    email: str
    role_id: int
    password: str | None = None


@dataclass
class CreateUserResult:
    user: User
    generated_password: str | None


class CreateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHash,
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def execute(self, data: CreateUserData) -> CreateUserResult:
        existing_user = await self._user_repository.find_by_email(data.email)

        if existing_user is not None:
            raise UserAlreadyExistsError("User with this email already exists")

        generated_password = None
        password = data.password

        if password is None:
            generated_password = secrets.token_urlsafe(16)
            password = generated_password

        hashed_password = self._password_hasher.hash(password)

        user = User(
            name=data.name,
            email=data.email,
            password=hashed_password,
            role_id=data.role_id,
            created_at=date.today(),
        )

        created_user = await self._user_repository.create(user)

        return CreateUserResult(
            user=created_user,
            generated_password=generated_password,
        )