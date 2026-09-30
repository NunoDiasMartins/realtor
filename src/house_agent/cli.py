"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from house_agent.config import load_settings
from house_agent.db import initialize_database
from house_agent.logging import configure_logging
from house_agent.pipeline import collect
from house_agent.repository import ListingRepository
from house_agent.sources.fixture import FixtureSource


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="house-agent")
    subparsers = parser.add_subparsers(dest="command", required=True)
    collect_parser = subparsers.add_parser("collect", help="collect property listings")
    collect_parser.add_argument("--source", choices=("fixture",), required=True)
    collect_parser.add_argument("--config", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    settings = load_settings(args.config)
    configure_logging(settings.log_level)

    if args.command == "collect" and args.source == "fixture":
        engine = initialize_database(settings.database_url)
        try:
            result = collect(
                FixtureSource(settings.fixture_path),
                ListingRepository(engine),
                settings,
            )
        finally:
            engine.dispose()
        print(json.dumps(result.model_dump(), sort_keys=True))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
