"""Inventory.py schemas."""

from app.schemas.library import LibraryRead
from app.schemas.material import MaterialRead
from shared.utils.deps import ConfigModel


class InventoryBase(ConfigModel):
    """InventoryBase schema."""

    stock: int
    material_id: int
    library_id: int


class InventoryCreate(InventoryBase):
    """InventoryCreate schema."""


class Inventory(InventoryBase):
    """Inventory schema."""

    id: int


class InventoryRead(Inventory):
    """InventoryRead schema."""

    library: LibraryRead
    material: MaterialRead


class InventoryUpdate(ConfigModel):
    """InventoryUpdate schema."""

    stock: int | None = None
    material_id: int | None = None
    library_id: int | None = None
