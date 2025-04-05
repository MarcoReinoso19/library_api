"""auth_service.py."""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.permission import DBPermission
from app.models.user import DBUser
from app.schemas.token import (
    AccessToken,
    AccessTokenCreate,
)
from app.services.user_service import (
    db_read_user_by_email_or_username,
    db_read_user_permissions_by_library,
)
from config.settings import settings
from shared.utils.deps import CurrentUserDep
from shared.utils.errors import (
    AuthorizationError,
    InvalidCredentialsError,
    NotFoundError,
)


def authenticate_user(
    session: Session,
    username: str,
    password: str,
) -> DBUser:
    """Authenticate user."""
    try:
        user = db_read_user_by_email_or_username(
            session=session, email_or_username=username
        )
    except NotFoundError:
        raise InvalidCredentialsError
    if not verify_password(password, user.password):
        raise InvalidCredentialsError
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the plain password matches the hashed password."""
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Get password hash."""
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def create_auth_token(token: AccessTokenCreate) -> str:
    """Create authentication token."""
    if token.expires_delta:
        expire = datetime.now(timezone.utc) + token.expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode: AccessToken = AccessToken(
        subject=token.subject,
        scopes=token.scopes,
        expire=expire,
    )

    encoded_jwt = jwt.encode(
        to_encode.model_dump(
            mode="json"
        ),  # JSON mode required for Datetime serialization
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


def get_token_default_expire_time() -> timedelta:
    """Get token default expire time."""
    return timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def check_permissions(
    permission_name: str,
    library_id: int,
    current_user: CurrentUserDep,
    session: Session,
) -> bool:
    """Check permissions."""
    user_permissions = db_read_user_permissions_by_library(
        session=session,
        user_id=current_user.id,
        library_id=library_id,
    )

    if not user_permissions:
        raise AuthorizationError("Any permission for this library")

    permissions = (
        session.query(DBPermission)
        .filter(
            DBPermission.id.in_(
                [permission.permission_id for permission in user_permissions]
            )
        )
        .all()
    )
    for permission in permissions:
        if permission.name == permission_name:
            return True
    raise AuthorizationError("Permission denied for this library")
