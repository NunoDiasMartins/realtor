"""Validated models used at pipeline boundaries."""

from __future__ import annotations

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, field_validator


class FixtureListing(BaseModel):
    """Schema accepted from fixture JSON files."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    id: str = Field(min_length=1)
    url: AnyHttpUrl
    title: str = Field(min_length=1)
    price: int = Field(gt=0)
    currency: str = Field(min_length=3, max_length=3)
    bedrooms: int = Field(ge=0)
    area_sqm: float = Field(gt=0)
    location: str = Field(min_length=1)
    description: str | None = None
    property_type: str | None = None

    @field_validator("description", "property_type", mode="before")
    @classmethod
    def blank_optional_strings_are_none(cls, value: object) -> object:
        return None if isinstance(value, str) and not value.strip() else value


class NormalizedListing(BaseModel):
    """Canonical listing representation used by filtering and persistence."""

    model_config = ConfigDict(frozen=True)

    source: str
    source_id: str
    url: str
    title: str
    price: int
    currency: str
    bedrooms: int
    area_sqm: float
    location: str
    description: str | None = None
    property_type: str | None = None


class FilterResult(BaseModel):
    passed: bool
    reasons: tuple[str, ...] = ()


class CollectionResult(BaseModel):
    loaded: int = 0
    passed: int = 0
    rejected: int = 0
    invalid: int = 0
    persisted: int = 0
    already_known: int = 0
    external_api_calls: int = 0
