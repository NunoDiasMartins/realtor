import json
from pathlib import Path

from house_agent.cli import main


def test_cli_collects_fixture_and_prints_summary(
    tmp_path: Path, fixture_path: Path, capsys
) -> None:
    config = tmp_path / "config.toml"
    config.write_text(
        f'''[house_agent]
database_url = "sqlite:///{tmp_path / "cli.db"}"
fixture_path = "{fixture_path}"
''',
        encoding="utf-8",
    )

    exit_code = main(["collect", "--source", "fixture", "--config", str(config)])

    assert exit_code == 0
    summary = json.loads(capsys.readouterr().out)
    assert summary["loaded"] == 5
    assert summary["passed"] == 3
    assert summary["rejected"] == 2
    assert summary["persisted"] == 3
    assert summary["external_api_calls"] == 0
