"""author_router.py."""

from fastapi import APIRouter, status

from app.schemas.author import (
    AuthorCreate,
    AuthorRead,
    AuthorUpdate,
)
from app.services.author_service import (
    db_create_author,
    db_delete_author,
    db_read_author,
    db_read_authors,
    db_update_author,
)
from shared.utils.deps import CurrentUserDep, SessionDep

router = APIRouter(prefix="/author", tags=["Author"])


@router.post("/", status_code=status.HTTP_201_CREATED)
# @authorize('author:create')
async def create_author(session: SessionDep, author: AuthorCreate) -> AuthorRead:
    """Endpoint to create a new author."""
    return AuthorRead.model_validate(db_create_author(session, author))


@router.get("/{author_id}", status_code=status.HTTP_200_OK)
# @authorize('author:read')
async def read_author(session: SessionDep, author_id: int) -> AuthorRead:
    """Endpoint to read an author."""
    return AuthorRead.model_validate(db_read_author(session, author_id))


@router.get("/", status_code=status.HTTP_200_OK)
# @authorize('author:read_all')
async def read_authors(session: SessionDep) -> list[AuthorRead]:
    """Endpoint to read all authors."""
    return [AuthorRead.model_validate(author) for author in db_read_authors(session)]


@router.patch("/{author_id}", status_code=status.HTTP_200_OK)
# @authorize('author:update')
async def update_author(
    session: SessionDep, author_id: int, author_updated: AuthorUpdate
) -> AuthorRead:
    """Endpoint to update a author."""
    return AuthorRead.model_validate(
        db_update_author(session, author_id, author_updated)
    )


@router.delete("/{author_id}", status_code=status.HTTP_200_OK)
# @authorize("author:delete")
async def delete_author(
    session: SessionDep, current_user: CurrentUserDep, author_id: int
) -> bool:
    """Endpoint to delete an author."""
    return db_delete_author(session, author_id)
