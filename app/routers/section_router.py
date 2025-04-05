"""section_router.py."""

from fastapi import APIRouter, status

from app.schemas.section import (
    SectionCreate,
    SectionRead,
    SectionUpdate,
)
from app.services.section_service import (
    db_create_section,
    db_delete_section,
    db_read_section,
    db_read_sections,
    db_update_section,
)
from shared.utils.deps import CurrentUserDep, SessionDep

router = APIRouter(prefix="/section", tags=["Section"])


@router.post("/", status_code=status.HTTP_201_CREATED)
# @authorize('section:create')
async def create_section(session: SessionDep, section: SectionCreate) -> SectionRead:
    """Endpoint to create a new section."""
    return SectionRead.model_validate(db_create_section(session, section))


@router.get("/{section_id}", status_code=status.HTTP_200_OK)
# @authorize('section:read')
async def read_section(session: SessionDep, section_id: int) -> SectionRead:
    """Endpoint to read an section."""
    return SectionRead.model_validate(db_read_section(session, section_id))


@router.get("/", status_code=status.HTTP_200_OK)
# @authorize('section:read_all')
async def read_sections(session: SessionDep) -> list[SectionRead]:
    """Endpoint to read all sections."""
    return [
        SectionRead.model_validate(section) for section in db_read_sections(session)
    ]


@router.patch("/{section_id}", status_code=status.HTTP_200_OK)
# @authorize('section:update')
async def update_section(
    session: SessionDep, section_id: int, section_updated: SectionUpdate
) -> SectionRead:
    """Endpoint to update a section."""
    return SectionRead.model_validate(
        db_update_section(session, section_id, section_updated)
    )


@router.delete("/{section_id}", status_code=status.HTTP_200_OK)
# @authorize("section:delete")
async def delete_section(
    session: SessionDep, current_user: CurrentUserDep, section_id: int
) -> bool:
    """Endpoint to delete an section."""
    return db_delete_section(session, section_id)
