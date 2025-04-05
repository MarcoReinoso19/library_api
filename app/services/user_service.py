"""contact_service.py."""

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.library import DBLibrary
from app.models.role import DBRole
from app.models.role_permissions import DBRolePermission
from app.models.user import DBUser
from app.models.user_roles import DBUserRole
from app.schemas.user import UserCreate, UserUpdate
from shared.utils.deps import commit_and_refresh
from shared.utils.errors import AuthorizationError, NotFoundError
from shared.utils.validations import (
    validate_email_format,
    validate_entity_existence,
    validate_unique_constraints,
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Get password hash."""
    return pwd_context.hash(password)


def db_create_user(session: Session, user: UserCreate) -> DBUser:
    """Create a new user in the database."""
    validate_unique_constraints(session, DBUser, user)
    validate_email_format(user.email)

    # Crear una copia del usuario y modificar la contraseña
    modify_user = user.model_copy()
    modify_user.password = get_password_hash(user.password)

    new_user: DBUser = DBUser(**modify_user.model_dump(exclude_none=True))
    return commit_and_refresh(session, new_user)


def db_read_user(session: Session, user_id: int) -> DBUser:
    """Read a user from the database."""
    return validate_entity_existence(session, DBUser, user_id)


def db_read_user_by_email(session: Session, email: str) -> DBUser:
    """Read a user from the database by email."""
    user = session.query(DBUser).filter(DBUser.email == email).first()
    if not user:
        raise NotFoundError("User")
    return user


def db_read_user_by_username(session: Session, username: str) -> DBUser:
    """Read a user from the database by username."""
    user = session.query(DBUser).filter(DBUser.username == username).first()
    if not user:
        raise NotFoundError("User", "username", username)

    return user


def db_read_user_by_email_or_username(
    session: Session, email_or_username: str
) -> DBUser:
    """Read a user from the database by email or username."""
    try:
        user = db_read_user_by_email(session=session, email=email_or_username)
    except NotFoundError:
        user = db_read_user_by_username(session=session, username=email_or_username)
    return user


def db_read_user_roles_by_library(
    session: Session, user_id: int, library_id: int
) -> list[DBUserRole]:
    """Read the roles of a user in a library from the database."""
    user = db_read_user(session=session, user_id=user_id)
    if library_id not in [org.id for org in user.libraries]:
        raise AuthorizationError
    user_roles = (
        session.query(DBUserRole)
        .filter(DBUserRole.user_id == user_id, DBUserRole.library_id == library_id)
        .all()
    )
    return user_roles


def db_read_user_permissions_by_library(
    session: Session, user_id: int, library_id: int
) -> list[DBRolePermission]:
    """Read the permissions of a user in an library from the database."""
    user_roles = db_read_user_roles_by_library(
        session=session, user_id=user_id, library_id=library_id
    )
    roles_ids = [role.role_id for role in user_roles]
    permissions = (
        session.query(DBRolePermission)
        .filter(DBRolePermission.role_id.in_(roles_ids))
        .all()
    )
    return permissions


def db_read_user_libraries(session: Session, user_id: int) -> list[DBLibrary]:
    """Read the libraries of a user from the database."""
    user = db_read_user(session=session, user_id=user_id)
    return user.libraries


def db_read_user_library_roles(
    session: Session, user_id: int, library_id: int
) -> list[DBRole]:
    """Read the roles of a user in an library from the database."""
    user = db_read_user(session=session, user_id=user_id)
    if library_id not in [org.id for org in user.libraries]:
        raise NotFoundError("Library", "id", library_id)
    user_roles = (
        session.query(DBUserRole)
        .filter(DBUserRole.user_id == user_id, DBUserRole.library_id == library_id)
        .all()
    )
    if not user_roles:
        raise NotFoundError("Roles")
    roles: list[DBRole] = [user_role.role for user_role in user_roles]
    return roles


def db_read_user_library_with_roles(
    session: Session, user_id: int, library_id: int
) -> list[DBRole]:
    """Read the roles of a user in an library from the database."""
    user = db_read_user(session=session, user_id=user_id)
    if library_id not in [org.id for org in user.libraries]:
        raise NotFoundError("Library", "id", library_id)
    user_roles = (
        session.query(DBUserRole)
        .filter(DBUserRole.user_id == user_id, DBUserRole.library_id == library_id)
        .all()
    )
    if not user_roles:
        raise NotFoundError("Roles")

    roles: list[DBRole] = [user_role.role for user_role in user_roles]
    return roles


def db_update_user(session: Session, user_id: int, user_updated: UserUpdate) -> DBUser:
    """Update a user in the database."""
    validate_unique_constraints(session, DBUser, user_updated)
    user = db_read_user(session=session, user_id=user_id)
    user_data = user_updated.model_dump(exclude_unset=True)
    for field, value in user_data.items():
        setattr(user, field, value)
    return commit_and_refresh(session, user)
