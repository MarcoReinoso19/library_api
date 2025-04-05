"""role_permission.py model."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class DBRolePermission(Base):
    """RolePermissions model."""

    __tablename__ = "role_permissions"
    # Required fields
    id = None  # type: ignore

    # Foreign keys
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"), primary_key=True
    )
