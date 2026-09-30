"""Listing persistence operations."""

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from house_agent.db import ListingRecord
from house_agent.models import NormalizedListing


class ListingRepository:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def add_if_new(self, listing: NormalizedListing) -> bool:
        """Insert a listing once; return false when its source identity exists."""

        with Session(self.engine) as session:
            existing = session.scalar(
                select(ListingRecord.id).where(
                    ListingRecord.source == listing.source,
                    ListingRecord.source_id == listing.source_id,
                )
            )
            if existing is not None:
                return False
            session.add(ListingRecord(**listing.model_dump()))
            session.commit()
            return True
