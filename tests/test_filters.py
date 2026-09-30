from house_agent.filters import apply_hard_filters
from house_agent.models import NormalizedListing


def listing(**changes) -> NormalizedListing:
    values = {
        "source": "fixture",
        "source_id": "one",
        "url": "https://example.test/one",
        "title": "Home",
        "price": 400000,
        "currency": "EUR",
        "bedrooms": 3,
        "area_sqm": 90,
        "location": "Lisbon",
    }
    values.update(changes)
    return NormalizedListing.model_validate(values)


def test_listing_at_thresholds_passes(settings) -> None:
    result = apply_hard_filters(
        listing(
            price=settings.max_price,
            bedrooms=settings.min_bedrooms,
            area_sqm=settings.min_area_sqm,
        ),
        settings,
    )
    assert result.passed
    assert result.reasons == ()


def test_reports_every_failed_hard_filter(settings) -> None:
    result = apply_hard_filters(
        listing(price=600000, bedrooms=1, area_sqm=50), settings
    )
    assert not result.passed
    assert result.reasons == (
        "price_above_maximum",
        "bedrooms_below_minimum",
        "area_below_minimum",
    )
