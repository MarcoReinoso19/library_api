"""material.py model."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.section import DBSection
from shared.utils.enums import MaterialType

if TYPE_CHECKING:
    from app.models.author import DBAuthor
else:
    DBAuthor = "DBAuthor"


class DBMaterial(Base):
    """Material model."""

    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[MaterialType]
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    cod_ref: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    price: Mapped[float] = mapped_column(nullable=False)
    isbn: Mapped[str] = mapped_column(nullable=True, default=None)
    issn: Mapped[str] = mapped_column(nullable=True, default=None)
    description: Mapped[str] = mapped_column(nullable=True, default=None)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"))

    author: Mapped[DBAuthor] = relationship(back_populates="materials")
    section: Mapped[DBSection] = relationship()
