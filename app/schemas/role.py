"""role.py schemas."""

from shared.utils.deps import ConfigModel


class RoleBase(ConfigModel):
    """RoleBase schema."""

    name: str
    code: str
    description: str


class RoleCreate(RoleBase):
    """RoleCreate schema."""


class Role(RoleBase):
    """Role schema."""

    id: int


class RoleRead(Role):
    """RoleRead schema."""


class RoleUpdate(ConfigModel):
    """RoleUpdate schema."""

    name: str | None = None
    code: str | None = None
    description: str | None = None
