"""library_service.py."""

from sqlalchemy.orm import Session

from app.models.library import DBLibrary
from app.models.library_users import DBLibraryUser
from app.models.user import DBUser
from app.models.user_roles import DBUserRole
from app.schemas.library import (
    LibraryCreate,
    LibraryUpdate,
)
from app.services.role_service import db_read_role
from app.services.user_service import db_read_user
from shared.utils.deps import (
    commit_and_refresh,
)
from shared.utils.errors import DeleteError, NotFoundError
from shared.utils.validations import (
    validate_entity_existence,
    validate_unique_constraints,
)


def db_create_library(
    session: Session, library: LibraryCreate, user_id: int
) -> DBLibrary:
    """Create a new library in the database."""
    validate_unique_constraints(session, DBLibrary, library)
    new_library = DBLibrary(**library.model_dump(exclude_none=True))
    db_library = commit_and_refresh(session, new_library)

    db_add_library_user(
        session=session, library_id=db_library.id, user_id=user_id, role_id=1
    )

    return commit_and_refresh(session, new_library)


def db_read_library(
    session: Session,
    library_id: int,
) -> DBLibrary:
    """Read a library from the database."""
    return validate_entity_existence(session, DBLibrary, library_id)


def db_read_library_users(session: Session, library_id: int) -> list[DBUser]:
    """Read the users of an library from the database."""
    library = db_read_library(session=session, library_id=library_id)

    return library.users


def db_read_libraries_me(session: Session, current_user_id: int) -> list[DBLibrary]:
    """Read the libraries of a user from the database."""
    user = db_read_user(session=session, user_id=current_user_id)

    return user.libraries


def db_add_library_user(
    session: Session, library_id: int, user_id: int, role_id: int
) -> DBLibraryUser:
    """Add a user to an library in the database."""
    library = db_read_library(session=session, library_id=library_id)
    if not library:
        raise NotFoundError(DBLibrary.__name__, "id", library_id)
    user = db_read_user(session=session, user_id=user_id)
    if not user:
        raise NotFoundError(DBUser.__name__, "id", user_id)
    role = db_read_role(session=session, role_id=role_id)

    library_user = (
        session.query(DBLibraryUser)
        .filter_by(library_id=library.id, user_id=user.id)
        .first()
    )
    if library_user:
        user_role = (
            session.query(DBUserRole)
            .filter_by(library_id=library.id, user_id=user.id, role_id=role.id)
            .first()
        )
        if user_role:
            raise ValueError(
                f"User {user.id} already has role {role.id} in library {library.id}."
            )
        else:
            user_role = DBUserRole(
                user_id=user.id, role_id=role.id, library_id=library.id
            )
            session.add(user_role)
            commit_and_refresh(session, user_role)
            return library_user
    else:
        library_user = DBLibraryUser(user_id=user.id, library_id=library.id)
        member_role = DBUserRole(
            user_id=user.id, role_id=role.id, library_id=library.id
        )

        commit_and_refresh(session, member_role)

    return commit_and_refresh(session, library_user)


def db_update_library(
    session: Session,
    library_id: int,
    library_updated: LibraryUpdate,
) -> DBLibrary:
    """Update a library in the database."""
    validate_unique_constraints(session, DBLibrary, library_updated)
    library = db_read_library(session=session, library_id=library_id)
    library_data = library_updated.model_dump(exclude_unset=True)
    for field, value in library_data.items():
        setattr(library, field, value)
    return commit_and_refresh(session, library)


def db_delete_library(session: Session, library_id: int) -> bool:
    """Delete a library from the database."""
    library = db_read_library(session=session, library_id=library_id)
    if not library:
        raise NotFoundError("library", "id", library_id)
    try:
        session.delete(library)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise DeleteError("library")
