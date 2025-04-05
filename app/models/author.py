"""author.py model."""

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.material import DBMaterial


class DBAuthor(Base):
    """Author model."""

    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)

    materials: Mapped[list[DBMaterial]] = relationship(back_populates="author")
