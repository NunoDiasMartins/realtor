# House Hunting Agent

This repository implements Phases 1 and 2 of a local-first house-hunting agent.
It loads JSON fixture listings, validates and normalizes them, applies deterministic
hard filters, and persists passing listings to SQLite without creating duplicates.

## Requirements and installation

- Python 3.12+

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Usage

```bash
house-agent collect --source fixture
```

The bundled fixture contains five listings. With the defaults, three pass and two
are rejected. On the first run, the three passing listings are inserted. On later
runs they are reported as already known and no duplicate rows are created.

Use a configuration file with `--config path/to/config.toml`:

```toml
[house_agent]
database_url = "sqlite:///house_agent.db"
fixture_path = "fixtures/listings.json"
max_price = 500000
min_bedrooms = 2
min_area_sqm = 70
log_level = "INFO"
```

Every setting can be overridden with an uppercase `HOUSE_AGENT_` environment
variable, for example `HOUSE_AGENT_MAX_PRICE=450000`. Relative `fixture_path`
values in a TOML file are resolved relative to that file. SQLite tables are
created automatically when collection starts. Logs are JSON and are written to
stderr; the collection summary is JSON on stdout.

## Architecture

- `config.py`: typed TOML/environment configuration.
- `models.py`: source-boundary, normalized, and result Pydantic models.
- `sources/`: the source protocol and local JSON fixture adapter.
- `normalization.py`: pure canonicalization into the normalized schema.
- `filters.py`: deterministic, configurable hard filters.
- `db.py` and `repository.py`: SQLAlchemy schema, initialization, and idempotent
  persistence using the unique `(source, source_id)` identity.
- `pipeline.py`: orchestration and collection counters.
- `cli.py`: the `house-agent collect --source fixture` command.

## Tests

```bash
pytest
```

The tests cover configuration, fixture loading, normalization, hard filtering,
persistence, idempotent reruns, and CLI execution.

## Current limitations

Only local JSON fixtures are supported. There are no portal integrations, browser
automation, external API calls, LLM evaluation, notifications, scheduling,
cross-source fuzzy deduplication, price history, or ranking beyond hard-filter
acceptance. Listings are updated only by adding new unique source identities;
existing rows are deliberately left unchanged in this phase.

## Recommended next step

Define Phase 3's source contract and operational requirements, then add one
licensed HTTP/API-backed source adapter with rate limiting and recorded contract
tests while retaining the same normalization and persistence boundaries.

