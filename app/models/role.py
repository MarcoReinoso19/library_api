"""role.py model."""

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DBRole(Base):
    """Role model."""

    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    code: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True, default=None)
