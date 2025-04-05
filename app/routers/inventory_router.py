"""inventory_router.py."""

from fastapi import APIRouter, status

from app.schemas.inventory import (
    InventoryCreate,
    InventoryRead,
    InventoryUpdate,
)
from app.services.inventory_service import (
    db_add_to_inventory,
    db_delete_inventory,
    db_read_inventories_me,
    db_read_inventory_item,
    db_update_inventory,
)
from shared.utils.decorators import authorize
from shared.utils.deps import CurrentUserDep, SessionDep

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/", status_code=status.HTTP_201_CREATED)
# @authorize('inventory:create')
async def add_to_inventory(
    session: SessionDep, inventory: InventoryCreate
) -> InventoryRead:
    """Endpoint to add a new item to inventory."""
    return InventoryRead.model_validate(db_add_to_inventory(session, inventory))


@router.get("/item/", status_code=status.HTTP_200_OK)
@authorize("inventory:read")
async def read_inventory_item(
    session: SessionDep, current_user: CurrentUserDep, library_id: int, material_id: int
) -> InventoryRead:
    """Endpoint to read an item of an inventory."""
    return InventoryRead.model_validate(
        db_read_inventory_item(session, library_id, material_id)
    )


@router.get("/me/", status_code=status.HTTP_200_OK)
# @authorize("inventory:read")
async def read_inventories_me(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[InventoryRead]:
    """Endpoint to read my inventories."""
    return [
        InventoryRead.model_validate(item)
        for item in db_read_inventories_me(session, current_user.id)
    ]


@router.patch("/{inventory_id}", status_code=status.HTTP_200_OK)
# @authorize("inventory:update")
async def update_inventory(
    session: SessionDep,
    current_user: CurrentUserDep,
    inventory_id: int,
    inventory_updated: InventoryUpdate,
) -> InventoryRead:
    """Endpoint to update a inventory."""
    return InventoryRead.model_validate(
        db_update_inventory(session, inventory_id, inventory_updated)
    )


@router.delete("/{inventory_id}", status_code=status.HTTP_200_OK)
@authorize("inventory:delete")
async def delete_inventory(
    session: SessionDep, current_user: CurrentUserDep, inventory_id: int
) -> bool:
    """Endpoint to delete an inventory."""
    return db_delete_inventory(session, inventory_id)
