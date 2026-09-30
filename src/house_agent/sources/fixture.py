"""Local JSON fixture source."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import TypeAdapter

from house_agent.models import FixtureListing


class FixtureSource:
    name = "fixture"

    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> list[FixtureListing]:
        with self.path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        return TypeAdapter(list[FixtureListing]).validate_python(payload)
