"""library_user.py schemas."""

from shared.utils.deps import ConfigModel


class LibraryUserBase(ConfigModel):
    """LibraryUserBase schema."""

    # Foreign keys
    library_id: int
    user_id: int


class LibraryUserCreate(LibraryUserBase):
    """LibraryUserCreate schema."""


class LibraryUser(LibraryUserBase):
    """LibraryUser schema."""


class LibraryUserRead(LibraryUser):
    """LibraryUserRead schema."""


class LibraryUserUpdate(ConfigModel):
    """UserUpdate schema."""

    library_id: int | None = None
    user_id: int | None = None
