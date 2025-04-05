"""Inventory.py."""

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.library import DBLibrary
from app.models.material import DBMaterial


class DBInventory(Base):
    """Inventory model."""

    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    stock: Mapped[int] = mapped_column(nullable=False, default=0)
    material_id: Mapped[int] = mapped_column(ForeignKey("materials.id"))
    library_id: Mapped[int] = mapped_column(ForeignKey("libraries.id"))

    library: Mapped[DBLibrary] = relationship()
    material: Mapped[DBMaterial] = relationship()

    __table_args__ = (
        UniqueConstraint("library_id", "material_id", name="unique_library_material"),
    )
