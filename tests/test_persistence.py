from sqlalchemy import func, select
from sqlalchemy.orm import Session

from house_agent.db import ListingRecord, initialize_database
from house_agent.models import NormalizedListing
from house_agent.repository import ListingRepository


def test_persists_once_by_source_identity(settings) -> None:
    engine = initialize_database(settings.database_url)
    repository = ListingRepository(engine)
    listing = NormalizedListing(
        source="fixture",
        source_id="123",
        url="https://example.test/123",
        title="Home",
        price=400000,
        currency="EUR",
        bedrooms=2,
        area_sqm=80,
        location="Lisbon",
    )

    assert repository.add_if_new(listing)
    assert not repository.add_if_new(listing)
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(ListingRecord)) == 1
    engine.dispose()
