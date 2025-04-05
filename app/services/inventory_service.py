"""inventory_service.py."""

from sqlalchemy.orm import Session

from app.models.inventory import DBInventory
from app.schemas.inventory import InventoryCreate, InventoryUpdate
from app.services.user_service import db_read_user
from shared.utils.deps import commit_and_refresh
from shared.utils.errors import DeleteError, NotFoundError
from shared.utils.validations import (
    validate_entity_existence,
    validate_unique_constraints,
)


def db_add_to_inventory(session: Session, inventory: InventoryCreate) -> DBInventory:
    """Add a new item to inventory in the database."""
    validate_unique_constraints(session, DBInventory, inventory)
    new_inventory_item = DBInventory(**inventory.model_dump(exclude_none=True))
    return commit_and_refresh(session, new_inventory_item)


def db_read_inventory(session: Session, inventory_id: int) -> DBInventory:
    """Read a inventory by id from the database."""
    return validate_entity_existence(session, DBInventory, inventory_id)


def db_read_inventory_item(
    session: Session, library_id: int, material_id: int
) -> DBInventory:
    """Read a inventory by id from the database."""
    inventory = (
        session.query(DBInventory)
        .filter_by(library_id=library_id, material_id=material_id)
        .first()
    )
    if not inventory:
        raise NotFoundError("inventory")
    return inventory


def db_read_inventories_me(session: Session, current_user_id: int) -> list[DBInventory]:
    """Read a my inventories from the database."""
    user = db_read_user(session, current_user_id)
    libraries = user.libraries

    inventories = (
        session.query(DBInventory)
        .filter(DBInventory.library_id.in_([library.id for library in libraries]))
        .all()
    )

    if not inventories:
        raise NotFoundError("inventories")
    return inventories


def db_update_inventory(
    session: Session,
    inventory_id: int,
    inventory_updated: InventoryUpdate,
) -> DBInventory:
    """Update a inventory in the database."""
    validate_unique_constraints(session, DBInventory, inventory_updated)
    db_inventory = db_read_inventory(session, inventory_id)
    inventory_data = inventory_updated.model_dump(exclude_unset=True)
    for field, value in inventory_data.items():
        setattr(db_inventory, field, value)
    return commit_and_refresh(session, db_inventory)


def db_delete_inventory(session: Session, inventory_id: int) -> bool:
    """Delete a inventory from the database."""
    inventory = db_read_inventory(session, inventory_id)
    if not inventory:
        raise NotFoundError("inventory")
    try:
        session.delete(inventory)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise DeleteError("inventory")
