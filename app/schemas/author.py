"""Author.py schemas."""

from shared.utils.deps import ConfigModel


class AuthorBase(ConfigModel):
    """AuthorBase schema."""

    name: str


class AuthorCreate(AuthorBase):
    """AuthorCreate schema."""


class Author(AuthorBase):
    """Author schema."""

    id: int


class AuthorRead(Author):
    """AuthorRead schema."""


class AuthorUpdate(ConfigModel):
    """AuthorUpdate schema."""

    name: str | None = None
