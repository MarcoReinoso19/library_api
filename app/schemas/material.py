"""Material.py schemas."""

from app.schemas.author import AuthorRead
from app.schemas.section import SectionRead
from shared.utils.deps import ConfigModel
from shared.utils.enums import MaterialType


class MaterialBase(ConfigModel):
    """MaterialBase schema."""

    type: MaterialType
    title: str
    cod_ref: str
    price: float
    isbn: str | None = None
    issn: str | None = None
    description: str | None = None

    author_id: int
    section_id: int


class MaterialCreate(MaterialBase):
    """MaterialCreate schema."""


class Material(MaterialBase):
    """Material schema."""

    id: int


class MaterialRead(Material):
    """MaterialRead schema."""

    author: AuthorRead
    section: SectionRead


class MaterialUpdate(ConfigModel):
    """MaterialUpdate schema."""

    type: MaterialType | None = None
    title: str | None = None
    cod_ref: str | None = None
    price: float | None = None
    isbn: str | None = None
    issn: str | None = None
    description: str | None = None

    author_id: int | None = None
    section_id: int | None = None
