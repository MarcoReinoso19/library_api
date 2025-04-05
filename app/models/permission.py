"""permission.py model."""

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DBPermission(Base):
    """Permission model."""

    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str | None] = mapped_column(default=None, nullable=True)
