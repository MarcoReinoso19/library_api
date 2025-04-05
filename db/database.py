"""database.py."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.base import Base

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)
SessionLocal = sessionmaker(bind=engine)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    from app import models  # noqa: F401 #  type: ignore

    Base.metadata.create_all(engine)
