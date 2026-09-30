"""Application configuration loaded from TOML and environment variables."""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


DEFAULT_FIXTURE_PATH = Path(__file__).parent / "fixtures" / "listings.json"


class Settings(BaseModel):
    """Validated runtime configuration."""

    model_config = ConfigDict(extra="forbid")

    database_url: str = "sqlite:///house_agent.db"
    fixture_path: Path = DEFAULT_FIXTURE_PATH
    max_price: int = Field(default=500_000, gt=0)
    min_bedrooms: int = Field(default=2, ge=0)
    min_area_sqm: float = Field(default=70, ge=0)
    log_level: str = "INFO"


_ENV_CASTERS = {
    "database_url": str,
    "fixture_path": Path,
    "max_price": int,
    "min_bedrooms": int,
    "min_area_sqm": float,
    "log_level": str,
}


def load_settings(path: Path | None = None) -> Settings:
    """Load defaults, an optional TOML file, then environment overrides."""

    values: dict[str, Any] = {}
    if path is not None:
        config_path = path.expanduser().resolve()
        with config_path.open("rb") as handle:
            document = tomllib.load(handle)
        values = dict(document.get("house_agent", {}))
        fixture_path = values.get("fixture_path")
        if fixture_path is not None and not Path(fixture_path).is_absolute():
            values["fixture_path"] = config_path.parent / fixture_path

    for name, caster in _ENV_CASTERS.items():
        env_value = os.getenv(f"HOUSE_AGENT_{name.upper()}")
        if env_value is not None:
            values[name] = caster(env_value)
    return Settings.model_validate(values)
