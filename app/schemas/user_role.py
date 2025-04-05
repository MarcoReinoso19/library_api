"""user_role.py schemas."""

from app.schemas.role import Role
from shared.utils.deps import ConfigModel


class UserRoleBase(ConfigModel):
    """UserRoleBase schema."""

    user_id: int
    role_id: int
    library_id: int


class UserRoleCreate(UserRoleBase):
    """UserRoleCreate schema."""


class UserRole(UserRoleBase):
    """UserRole schema."""

    role: Role


class UserRoleRead(UserRole):
    """UserRoleRead schema."""


class UserRoleUpdate(ConfigModel):
    """RoleUpdate schema."""

    user_id: int | None = None
    role_id: int | None = None
    library_id: int | None = None
