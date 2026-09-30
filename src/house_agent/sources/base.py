from typing import Protocol

from house_agent.models import FixtureListing


class ListingSource(Protocol):
    name: str

    def load(self) -> list[FixtureListing]: ...
