from typing import Protocol

from waimea_user_api.domain.entities.user import User


class UserRepository(Protocol):
    async def create(self, user: User) -> User: ...

    async def find_by_email(self, email: str) -> User | None: ...
