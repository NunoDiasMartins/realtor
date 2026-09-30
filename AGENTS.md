# Contributor guidance

## Scope

These instructions apply to the entire repository.

## Development

- Support Python 3.12 and later.
- Keep collection sources behind the `ListingSource` protocol.
- Keep normalization and filtering deterministic; they must not perform I/O.
- Use Pydantic models at input boundaries and SQLAlchemy for persistence.
- Add or update tests for every behavior change.
- Run `pytest` before committing.

## Project boundaries

Only local fixture collection is implemented in Phases 1 and 2. Do not add portal
scrapers, browser automation, external APIs, LLMs, notifications, semantic ranking,
fuzzy cross-source deduplication, or price history without a later phase request.

