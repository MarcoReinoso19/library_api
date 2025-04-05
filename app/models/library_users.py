"""library_users.py model."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DBLibraryUser(Base):
    """LibraryUsers model."""

    __tablename__ = "library_users"

    # Required fields
    # id must be None because it is a composite primary key
    id = None  # type: ignore

    # Foreign keys
    library_id: Mapped[int] = mapped_column(
        ForeignKey("libraries.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
