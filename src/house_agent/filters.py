"""Deterministic hard filters."""

from house_agent.config import Settings
from house_agent.models import FilterResult, NormalizedListing


def apply_hard_filters(listing: NormalizedListing, settings: Settings) -> FilterResult:
    reasons: list[str] = []
    if listing.price > settings.max_price:
        reasons.append("price_above_maximum")
    if listing.bedrooms < settings.min_bedrooms:
        reasons.append("bedrooms_below_minimum")
    if listing.area_sqm < settings.min_area_sqm:
        reasons.append("area_below_minimum")
    return FilterResult(passed=not reasons, reasons=tuple(reasons))
