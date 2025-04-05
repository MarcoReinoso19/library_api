"""User.py schemas."""

from shared.utils.deps import ConfigModel


class UserBase(ConfigModel):
    """UserBase schema."""

    username: str
    password: str
    email: str


class UserCreate(UserBase):
    """UserCreate schema."""


class User(UserBase):
    """User schema."""

    id: int


class UserRead(User):
    """UserRead schema."""


class UserUpdate(ConfigModel):
    """UserUpdate schema."""

    username: str | None = None
    password: str | None = None
    email: str | None = None
