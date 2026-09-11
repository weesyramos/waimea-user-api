from dataclasses import dataclass
from datetime import date


@dataclass
class User:
    name: str
    email: str
    password: str
    role_id: int
    id: int | None = None
    created_at: date | None = None
    updated_at: date | None = None