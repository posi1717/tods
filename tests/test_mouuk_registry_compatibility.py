from MOUUK.mouuk_registry import MOUUKRegistry
from uk_kb_collector.core.module_registry import ModuleRegistry


def test_legacy_registry_uses_all_canonical_modules():
    legacy = MOUUKRegistry()
    canonical = list(ModuleRegistry.load())

    assert len(legacy.list_modules()) == 34
    assert [item["code"] for item in legacy.list_modules()] == [module.code for module in canonical]


def test_legacy_registry_accepts_canonical_legacy_and_slug_identifiers():
    registry = MOUUKRegistry()

    assert registry.get_module_info("MOUUK-0001")["name"] == "Procurement Act 2023"
    assert registry.get_module_info("MOUUK_0001")["code"] == "MOUUK-0001"
    assert registry.get_module_info("ppn")["code"] == "MOUUK-0005"


def test_unknown_module_does_not_silently_fall_back():
    registry = MOUUKRegistry()

    try:
        registry.get_module_info("MOUUK-9999")
    except KeyError:
        pass
    else:
        raise AssertionError("unknown modules must raise KeyError")
