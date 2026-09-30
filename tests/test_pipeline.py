from sqlalchemy import func, select
from sqlalchemy.orm import Session

from house_agent.db import ListingRecord, initialize_database
from house_agent.pipeline import collect
from house_agent.repository import ListingRepository
from house_agent.sources.fixture import FixtureSource


def test_fixture_pipeline_is_idempotent(settings) -> None:
    engine = initialize_database(settings.database_url)
    repository = ListingRepository(engine)
    source = FixtureSource(settings.fixture_path)

    first = collect(source, repository, settings)
    second = collect(source, repository, settings)

    assert first.model_dump() == {
        "loaded": 5,
        "passed": 3,
        "rejected": 2,
        "invalid": 0,
        "persisted": 3,
        "already_known": 0,
        "external_api_calls": 0,
    }
    assert second.model_dump() == {
        "loaded": 5,
        "passed": 3,
        "rejected": 2,
        "invalid": 0,
        "persisted": 0,
        "already_known": 3,
        "external_api_calls": 0,
    }
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(ListingRecord)) == 3
    engine.dispose()
