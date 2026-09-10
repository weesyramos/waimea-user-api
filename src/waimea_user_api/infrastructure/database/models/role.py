from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from waimea_user_api.infrastructure.database.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(String, nullable=False)