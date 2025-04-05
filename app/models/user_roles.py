"""user_role.py model."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.role import DBRole


class DBUserRole(Base):
    """UserRole model."""

    __tablename__ = "user_roles"

    id = None  # type: ignore

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    library_id: Mapped[int] = mapped_column(
        ForeignKey("libraries.id"), primary_key=True
    )

    role: Mapped[DBRole] = relationship(
        overlaps="roles"
    )  # role for the user in the library
