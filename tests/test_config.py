from pathlib import Path

from house_agent.config import load_settings


def test_loads_toml_and_environment_override(tmp_path: Path, monkeypatch) -> None:
    fixture = tmp_path / "custom.json"
    config = tmp_path / "agent.toml"
    config.write_text(
        """[house_agent]
fixture_path = "custom.json"
max_price = 400000
min_bedrooms = 3
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("HOUSE_AGENT_MAX_PRICE", "450000")

    settings = load_settings(config)

    assert settings.fixture_path == fixture
    assert settings.max_price == 450_000
    assert settings.min_bedrooms == 3
