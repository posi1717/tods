from uk_kb_collector.core.module_registry import ModuleRegistry
from uk_kb_collector.intelligence import evaluate
from uk_kb_collector.workers import PluginManager, ReasoningRequest


def test_catalogue_contains_all_stable_module_codes():
    registry = ModuleRegistry.load()
    assert [module.code for module in registry] == [f"MOUUK-{number:04d}" for number in range(1, 35)]


def test_toms_is_owned_by_social_value():
    registry = ModuleRegistry.load()
    assert registry.get("toms").parent == "MOUUK-0011"


def test_plan_is_an_independent_reasoning_plugin():
    registry = ModuleRegistry.load()
    assert registry.get("MOUUK-0007").kind == "reasoning"


def test_intelligence_result_uses_stable_code():
    result = evaluate("authority", {"official": True}, confidence=0.9)
    assert result.engine_code == "MOUUK-0023"


def test_all_34_plugins_are_independently_loadable():
    workers = PluginManager().load_all()
    assert len(workers) == 34
    assert len({type(worker) for worker in workers}) == 34


def test_plugin_api_is_evidence_first():
    response = PluginManager().invoke("MOUUK-0001", ReasoningRequest("What applies?"))
    assert response.needs_review is True
    assert response.confidence == 0.0
