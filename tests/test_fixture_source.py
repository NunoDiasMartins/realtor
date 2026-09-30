import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from house_agent.sources.fixture import FixtureSource


def test_loads_five_valid_fixture_listings(fixture_path: Path) -> None:
    listings = FixtureSource(fixture_path).load()

    assert len(listings) == 5
    assert listings[1].description is None


def test_rejects_invalid_fixture_schema(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps([{"id": "missing-required-fields"}]), encoding="utf-8")

    with pytest.raises(ValidationError):
        FixtureSource(path).load()
