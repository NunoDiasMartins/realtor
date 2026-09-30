"""Collection pipeline orchestration."""

from __future__ import annotations

import logging

from house_agent.config import Settings
from house_agent.filters import apply_hard_filters
from house_agent.models import CollectionResult
from house_agent.normalization import normalize_listing
from house_agent.repository import ListingRepository
from house_agent.sources.base import ListingSource

logger = logging.getLogger(__name__)


def collect(
    source: ListingSource, repository: ListingRepository, settings: Settings
) -> CollectionResult:
    raw_listings = source.load()
    result = CollectionResult(loaded=len(raw_listings))

    for raw_listing in raw_listings:
        listing = normalize_listing(raw_listing, source.name)
        filter_result = apply_hard_filters(listing, settings)
        if not filter_result.passed:
            result.rejected += 1
            logger.info(
                "listing rejected: %s (%s)",
                listing.source_id,
                ",".join(filter_result.reasons),
            )
            continue

        result.passed += 1
        if repository.add_if_new(listing):
            result.persisted += 1
        else:
            result.already_known += 1

    logger.info("collection completed: %s", result.model_dump_json())
    return result
