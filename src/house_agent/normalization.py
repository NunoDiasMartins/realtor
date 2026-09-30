"""Pure listing normalization."""

from house_agent.models import FixtureListing, NormalizedListing


def normalize_listing(listing: FixtureListing, source: str) -> NormalizedListing:
    """Convert a validated source listing into its canonical representation."""

    return NormalizedListing(
        source=source.strip().lower(),
        source_id=listing.id.strip(),
        url=str(listing.url),
        title=" ".join(listing.title.split()),
        price=listing.price,
        currency=listing.currency.upper(),
        bedrooms=listing.bedrooms,
        area_sqm=listing.area_sqm,
        location=" ".join(listing.location.split()),
        description=(
            " ".join(listing.description.split()) if listing.description else None
        ),
        property_type=(
            listing.property_type.lower() if listing.property_type else None
        ),
    )
