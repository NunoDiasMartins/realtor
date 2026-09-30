from house_agent.models import FixtureListing
from house_agent.normalization import normalize_listing


def test_normalizes_text_currency_and_optional_blanks() -> None:
    raw = FixtureListing.model_validate(
        {
            "id": " abc ",
            "url": "https://example.test/abc",
            "title": "  A   sunny home ",
            "price": 300000,
            "currency": "eur",
            "bedrooms": 2,
            "area_sqm": 80,
            "location": "  Greater   Lisbon ",
            "description": " ",
            "property_type": " Apartment ",
        }
    )

    listing = normalize_listing(raw, " FIXTURE ")

    assert listing.source == "fixture"
    assert listing.source_id == "abc"
    assert listing.title == "A sunny home"
    assert listing.currency == "EUR"
    assert listing.location == "Greater Lisbon"
    assert listing.description is None
    assert listing.property_type == "apartment"
