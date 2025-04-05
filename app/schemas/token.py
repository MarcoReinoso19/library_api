"""token.py schema."""

from datetime import datetime, timedelta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.utils.deps import ConfigModel
else:
    from pydantic import BaseModel

    ConfigModel = BaseModel


class AccessToken(ConfigModel):
    """Token data class."""

    subject: str
    scopes: list[str] | None
    expire: datetime


class AccessTokenCreate(ConfigModel):
    """Token create class."""

    subject: str
    scopes: list[str] | None
    expires_delta: timedelta | None = None


class TokenSchema(ConfigModel):
    """TokenSchema schema."""

    access_token: str
