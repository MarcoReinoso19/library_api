"""author_service.py."""

from sqlalchemy.orm import Session

from app.models.author import DBAuthor
from app.schemas.author import AuthorCreate, AuthorUpdate
from shared.utils.deps import commit_and_refresh
from shared.utils.errors import DeleteError, NotFoundError
from shared.utils.validations import (
    validate_entity_existence,
    validate_unique_constraints,
)


def db_create_author(session: Session, author: AuthorCreate) -> DBAuthor:
    """Create a new author in the database."""
    validate_unique_constraints(session, DBAuthor, author)
    new_author = DBAuthor(**author.model_dump(exclude_none=True))
    return commit_and_refresh(session, new_author)


def db_read_author(session: Session, author_id: int) -> DBAuthor:
    """Read a author by id from the database."""
    return validate_entity_existence(session, DBAuthor, author_id)


def db_read_authors(session: Session) -> list[DBAuthor]:
    """Read all authors from the database."""
    return session.query(DBAuthor).all()


def db_update_author(
    session: Session, author_id: int, author_updated: AuthorUpdate
) -> DBAuthor:
    """Update a author in the database."""
    validate_unique_constraints(session, DBAuthor, author_updated)
    db_author = db_read_author(session=session, author_id=author_id)
    author_data = author_updated.model_dump(exclude_unset=True)
    for field, value in author_data.items():
        setattr(db_author, field, value)
    return commit_and_refresh(session, db_author)


def db_delete_author(session: Session, author_id: int) -> bool:
    """Delete a author from the database."""
    author = db_read_author(session=session, author_id=author_id)
    if not author:
        raise NotFoundError("author", "id", author_id)
    try:
        session.delete(author)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise DeleteError("author")
