"""library_router.py."""

from fastapi import APIRouter, status

from app.schemas.library import (
    LibraryCreate,
    LibraryRead,
    LibraryUpdate,
)
from app.schemas.library_user import LibraryUserRead
from app.schemas.user import UserRead
from app.services.library_service import (
    db_add_library_user,
    db_create_library,
    db_delete_library,
    db_read_libraries_me,
    db_read_library,
    db_read_library_users,
    db_update_library,
)
from shared.utils.decorators import authorize
from shared.utils.deps import CurrentUserDep, SessionDep

router = APIRouter(prefix="/library", tags=["Library"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_library(
    session: SessionDep,
    current_user: CurrentUserDep,
    library: LibraryCreate,
) -> LibraryRead:
    """Endpoint to create a new library."""
    return LibraryRead.model_validate(
        db_create_library(session, library, current_user.id)
    )


@router.get(
    "/{library_id}",
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def read_library(session: SessionDep, library_id: int) -> LibraryRead:
    """Endpoint to read a library."""
    return LibraryRead.model_validate(db_read_library(session, library_id))


@router.get("/users/{library_id}", status_code=status.HTTP_200_OK)
async def read_library_users(session: SessionDep, library_id: int) -> list[UserRead]:
    """Endpoint to read library users."""
    return [
        UserRead.model_validate(user)
        for user in db_read_library_users(session, library_id=library_id)
    ]


@router.get("/me/", status_code=status.HTTP_200_OK)
async def read_libraries_me(
    session: SessionDep, current_user: CurrentUserDep
) -> list[LibraryRead]:
    """Endpoint to read my library."""
    return [
        LibraryRead.model_validate(library)
        for library in db_read_libraries_me(session, current_user.id)
    ]


@router.post("/member", status_code=status.HTTP_201_CREATED)
async def add_library_member(
    session: SessionDep, library_id: int, user_id: int, role_id: int
) -> LibraryUserRead:
    """Endpoint to create a new library member."""
    return LibraryUserRead.model_validate(
        db_add_library_user(session, library_id, user_id, role_id)
    )


@router.patch("/{library_id}", status_code=status.HTTP_200_OK)
@authorize("library:update")
async def update_library(
    session: SessionDep,
    current_user: CurrentUserDep,
    library_id: int,
    library_updated: LibraryUpdate,
) -> LibraryRead:
    """Endpoint to update a library."""
    return LibraryRead.model_validate(
        db_update_library(session, library_id, library_updated)
    )


@router.delete("/{library_id}", status_code=status.HTTP_200_OK)
@authorize("library:delete")
async def delete_library(
    session: SessionDep, current_user: CurrentUserDep, library_id: int
) -> bool:
    """Endpoint to delete an library."""
    return db_delete_library(session, library_id)
