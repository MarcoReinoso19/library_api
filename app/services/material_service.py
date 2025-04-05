"""material_service.py."""

from sqlalchemy.orm import Session

from app.models.material import DBMaterial
from app.schemas.material import MaterialCreate, MaterialUpdate
from shared.utils.deps import commit_and_refresh
from shared.utils.errors import DeleteError, NotFoundError
from shared.utils.validations import (
    validate_entity_existence,
    validate_unique_constraints,
)


def db_create_material(session: Session, material: MaterialCreate) -> DBMaterial:
    """Create a new material in the database."""
    validate_unique_constraints(session, DBMaterial, material)
    new_material = DBMaterial(**material.model_dump(exclude_none=True))
    return commit_and_refresh(session, new_material)


def db_read_material(session: Session, material_id: int) -> DBMaterial:
    """Read a material by id from the database."""
    return validate_entity_existence(session, DBMaterial, material_id)


def db_read_materials(session: Session) -> list[DBMaterial]:
    """Read all materials from the database."""
    return session.query(DBMaterial).all()


def db_update_material(
    session: Session, material_id: int, material_updated: MaterialUpdate
) -> DBMaterial:
    """Update a material in the database."""
    validate_unique_constraints(session, DBMaterial, material_updated)
    db_material = db_read_material(session=session, material_id=material_id)
    material_data = material_updated.model_dump(exclude_unset=True)
    for field, value in material_data.items():
        setattr(db_material, field, value)
    return commit_and_refresh(session, db_material)


def db_delete_material(session: Session, material_id: int) -> bool:
    """Delete a material from the database."""
    material = db_read_material(session=session, material_id=material_id)
    if not material:
        raise NotFoundError("material", "id", material_id)
    try:
        session.delete(material)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise DeleteError("material")
