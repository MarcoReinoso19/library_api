"""section_service.py."""

from sqlalchemy.orm import Session

from app.models.section import DBSection
from app.schemas.section import SectionCreate, SectionUpdate
from shared.utils.deps import commit_and_refresh
from shared.utils.errors import DeleteError, NotFoundError
from shared.utils.validations import (
    validate_entity_existence,
    validate_unique_constraints,
)


def db_create_section(session: Session, section: SectionCreate) -> DBSection:
    """Create a new section in the database."""
    validate_unique_constraints(session, DBSection, section)
    new_section = DBSection(**section.model_dump(exclude_none=True))
    return commit_and_refresh(session, new_section)


def db_read_section(session: Session, section_id: int) -> DBSection:
    """Read a section by id from the database."""
    return validate_entity_existence(session, DBSection, section_id)


def db_read_sections(session: Session) -> list[DBSection]:
    """Read all sections from the database."""
    return session.query(DBSection).all()


def db_update_section(
    session: Session, section_id: int, section_updated: SectionUpdate
) -> DBSection:
    """Update a section in the database."""
    validate_unique_constraints(session, DBSection, section_updated)
    db_section = db_read_section(session=session, section_id=section_id)
    section_data = section_updated.model_dump(exclude_unset=True)
    for field, value in section_data.items():
        setattr(db_section, field, value)
    return commit_and_refresh(session, db_section)


def db_delete_section(session: Session, section_id: int) -> bool:
    """Delete a section from the database."""
    section = db_read_section(session=session, section_id=section_id)
    if not section:
        raise NotFoundError("section", "id", section_id)
    try:
        session.delete(section)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise DeleteError("section")
