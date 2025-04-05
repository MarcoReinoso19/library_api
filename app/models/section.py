"""Section.py."""

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DBSection(Base):
    """Section model."""

    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    capacity: Mapped[int]
