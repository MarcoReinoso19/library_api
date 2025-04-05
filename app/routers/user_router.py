"""user_router.py."""

from fastapi import APIRouter, status

from app.schemas.library import (
    LibraryRead,
)
from app.schemas.role import RoleRead
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import (
    db_create_user,
    db_read_user,
    db_read_user_by_email,
    db_read_user_by_username,
    db_read_user_libraries,
    db_read_user_library_roles,
    db_update_user,
)
from shared.utils.deps import (
    CurrentUserDep,
    SessionDep,
)

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(session: SessionDep, user: UserCreate) -> UserRead:
    """Endpoint to create a new user."""
    return UserRead.model_validate(db_create_user(session, user))


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(session: SessionDep, user_id: int) -> UserRead:
    """Endpoint to read a user."""
    return UserRead.model_validate(db_read_user(session, user_id))


@router.get("/username/{username}", status_code=status.HTTP_200_OK)
async def read_user_by_username(username: str, session: SessionDep) -> UserRead:
    """Endpoint to read a user by username."""
    return UserRead.model_validate(
        db_read_user_by_username(session=session, username=username)
    )


@router.get("/email/{email}", status_code=status.HTTP_200_OK)
# @authorize("user:create")
async def read_user_by_email(
    session: SessionDep, current_user: CurrentUserDep, email: str
) -> UserRead:
    """Endpoint to read a user by email."""
    return UserRead.model_validate(db_read_user_by_email(session, email))


@router.get("/me/libraries/", response_model_exclude_none=True)
async def read_user_me_libraries(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> list[LibraryRead]:
    """Endpoint to read user libraries."""
    return [
        LibraryRead.model_validate(library)
        for library in db_read_user_libraries(session, current_user.id)
    ]


@router.get("/me/library/role", status_code=status.HTTP_200_OK)
async def read_user_me_library_roles(
    session: SessionDep, current_user: CurrentUserDep, library_id: int
) -> list[RoleRead]:
    """Endpoint to read user library roles."""
    return [
        RoleRead.model_validate(role)
        for role in db_read_user_library_roles(session, current_user.id, library_id)
    ]


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    session: SessionDep,
    currentUser: CurrentUserDep,
    user_id: int,
    user_updated: UserUpdate,
) -> UserRead:
    """Endpoint to update a user."""
    return UserRead.model_validate(db_update_user(session, user_id, user_updated))
