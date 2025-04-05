"""auth router.py."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.token import AccessTokenCreate, TokenSchema
from app.schemas.user import UserRead
from app.schemas.user_role import UserRoleRead
from app.services.auth_service import (
    authenticate_user,
    create_auth_token,
    get_token_default_expire_time,
)
from app.services.user_service import db_read_user_roles_by_library
from shared.utils.deps import CurrentUserDep, SessionDep

router = APIRouter(tags=["Auth"])


@router.post(
    "/login",
    summary="Login to get an access token",
)
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    """Login to get an access token."""
    user = authenticate_user(session, form_data.username, form_data.password)
    # Create access token
    access_token = create_auth_token(
        AccessTokenCreate(
            subject=user.username,
            scopes=form_data.scopes,
            expires_delta=get_token_default_expire_time(),
        ),
    )

    # Return token schema with access and refresh tokens
    return TokenSchema(
        access_token=access_token,
    )


@router.get("/users/me")
async def read_users_me(
    current_user: CurrentUserDep,
) -> UserRead:
    """Read current user."""
    return UserRead.model_validate(current_user)


@router.get("/users/me/roles")
# @authorize("user:read")
async def read_users_me_with_role(
    session: SessionDep, current_user: CurrentUserDep, library_id: int
) -> list[UserRoleRead]:
    """Read current user roles."""
    return [
        UserRoleRead.model_validate(user_role)
        for user_role in db_read_user_roles_by_library(
            session,
            current_user.id,
            library_id,
        )
    ]


@router.post("/logout")
def user_logout(session: SessionDep, request: Request) -> dict[str, str]:
    """Logout."""

    return {"message": "Logout successful"}
