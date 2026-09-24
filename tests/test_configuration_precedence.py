from pathlib import Path

from uk_kb_collector.config import load_config


ROOT = Path(__file__).parents[1]


def test_root_config_is_the_active_collector_source():
    config = load_config(ROOT / "config.yaml")

    assert config.destination == (ROOT / "Knowledge_Base").resolve()
    assert config.sources
    assert config.allowed_domains


def test_parallel_reference_files_are_not_implicitly_merged():
    config = load_config(ROOT / "config.yaml")
    configured_urls = {source["url"] for source in config.sources}

    assert "https://www.gov.uk/government/collections/information-and-guidance-for-suppliers" not in configured_urls
