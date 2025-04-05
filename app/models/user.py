"""user.py model."""

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.library import DBLibrary
from app.models.library_users import DBLibraryUser
from app.models.role import DBRole
from app.models.user_roles import DBUserRole


class DBUser(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    libraries: Mapped[list[DBLibrary]] = relationship(
        secondary=DBLibraryUser.__table__, overlaps="users"
    )

    roles: Mapped[list[DBRole]] = relationship(
        secondary=DBUserRole.__table__, overlaps="roles"
    )
