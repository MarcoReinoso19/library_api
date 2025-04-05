"""Section.py schemas."""

from shared.utils.deps import ConfigModel


class SectionBase(ConfigModel):
    """SectionBase schema."""

    name: str
    capacity: int


class SectionCreate(SectionBase):
    """SectionCreate schema."""


class Section(SectionBase):
    """Section schema."""

    id: int


class SectionRead(Section):
    """SectionRead schema."""


class SectionUpdate(ConfigModel):
    """SectionUpdate schema."""

    name: str | None = None
    capacity: int | None = None
