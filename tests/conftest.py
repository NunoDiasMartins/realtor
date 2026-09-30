from pathlib import Path

import pytest

from house_agent.config import DEFAULT_FIXTURE_PATH, Settings


@pytest.fixture
def fixture_path() -> Path:
    return DEFAULT_FIXTURE_PATH


@pytest.fixture
def settings(tmp_path: Path, fixture_path: Path) -> Settings:
    return Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        fixture_path=fixture_path,
        max_price=500_000,
        min_bedrooms=2,
        min_area_sqm=70,
    )
