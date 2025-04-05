"""material_router.py."""

from fastapi import APIRouter, status

from app.schemas.material import (
    MaterialCreate,
    MaterialRead,
    MaterialUpdate,
)
from app.services.material_service import (
    db_create_material,
    db_delete_material,
    db_read_material,
    db_read_materials,
    db_update_material,
)
from shared.utils.decorators import authorize
from shared.utils.deps import CurrentUserDep, SessionDep

router = APIRouter(prefix="/material", tags=["Material"])


@router.post("/", status_code=status.HTTP_201_CREATED)
# @authorize('material:create')
async def create_material(
    session: SessionDep, material: MaterialCreate
) -> MaterialRead:
    """Endpoint to create a new material."""
    return MaterialRead.model_validate(db_create_material(session, material))


@router.get("/{material_id}", status_code=status.HTTP_200_OK)
# @authorize('material:read')
async def read_material(session: SessionDep, material_id: int) -> MaterialRead:
    """Endpoint to read an material."""
    return MaterialRead.model_validate(db_read_material(session, material_id))


@router.get("/", status_code=status.HTTP_200_OK)
# @authorize('material:read_all')
async def read_materials(session: SessionDep) -> list[MaterialRead]:
    """Endpoint to read all materials."""
    return [
        MaterialRead.model_validate(material) for material in db_read_materials(session)
    ]


@router.patch("/{material_id}", status_code=status.HTTP_200_OK)
@authorize("material:update")
async def update_material(
    session: SessionDep,
    current_user: CurrentUserDep,
    material_id: int,
    material_updated: MaterialUpdate,
) -> MaterialRead:
    """Endpoint to update a material."""
    return MaterialRead.model_validate(
        db_update_material(session, material_id, material_updated)
    )


@router.delete("/{material_id}", status_code=status.HTTP_200_OK)
@authorize("material:delete")
async def delete_material(
    session: SessionDep, current_user: CurrentUserDep, material_id: int
) -> bool:
    """Endpoint to delete an material."""
    return db_delete_material(session, material_id)
