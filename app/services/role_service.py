"""role_service.py."""

from sqlalchemy.orm import Session

from app.models.role import DBRole
from app.schemas.role import RoleCreate, RoleUpdate
from shared.utils.deps import commit_and_refresh
from shared.utils.errors import DeleteError, NotFoundError
from shared.utils.validations import (
    validate_entity_existence,
    validate_unique_constraints,
)


def db_create_role(session: Session, role: RoleCreate) -> DBRole:
    """Create a new role in the database."""
    validate_unique_constraints(session, DBRole, role)
    new_role = DBRole(**role.model_dump(exclude_none=True))
    return commit_and_refresh(session, new_role)


def db_read_role(session: Session, role_id: int) -> DBRole:
    """Read a role by id from the database."""
    return validate_entity_existence(session, DBRole, role_id)


def db_update_role(session: Session, role_id: int, role_updated: RoleUpdate) -> DBRole:
    """Update a role in the database."""
    validate_unique_constraints(session, DBRole, role_updated)
    db_role = db_read_role(session=session, role_id=role_id)
    role_data = role_updated.model_dump(exclude_unset=True)
    for field, value in role_data.items():
        setattr(db_role, field, value)
    return commit_and_refresh(session, db_role)


def db_delete_role(session: Session, role_id: int) -> bool:
    """Delete a role from the database."""
    role = db_read_role(session=session, role_id=role_id)
    if not role:
        raise NotFoundError("role", "id", role_id)
    try:
        session.delete(role)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise DeleteError("role")
