"""base.py."""

import inflect
from sqlalchemy.orm import DeclarativeBase

p = inflect.engine()


class Base(DeclarativeBase):
    """Base class for all models."""
