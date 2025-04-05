"""Library.py schemas."""

from shared.utils.deps import ConfigModel


class LibraryBase(ConfigModel):
    """LibraryBase schema."""

    name: str
    address: str


class LibraryCreate(LibraryBase):
    """LibraryCreate schema."""


class Library(LibraryBase):
    """Library schema."""

    id: int


class LibraryRead(Library):
    """LibraryRead schema."""


class LibraryUpdate(ConfigModel):
    """LibraryUpdate schema."""

    name: str | None = None
    address: str | None = None
