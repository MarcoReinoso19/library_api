"""library.py model."""

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.library_users import DBLibraryUser

if TYPE_CHECKING:
    from app.models.user import DBUser
else:
    DBUser = "DBUser"


class DBLibrary(Base):
    """Library model."""

    __tablename__ = "libraries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    address: Mapped[str] = mapped_column(unique=True)

    users: Mapped[list[DBUser]] = relationship(
        secondary=DBLibraryUser.__table__, overlaps="libraries"
    )
