from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ModuleDefinition:
    code: str
    slug: str
    name: str


# Deterministic routing from collector classification into the 26 MOUUK modules.
# Cross-cutting authority/temporal/relationship/evidence modules intentionally receive
# the same authoritative source as a reference copy; no text processing is performed.
CATEGORY_MODULES: dict[str, tuple[str, ...]] = {
    "01_Legislation/Procurement_Act_2023": ("MOUUK-0001",),
    "01_Legislation/Procurement_Regulations_2024": ("MOUUK-0002",),
    "01_Legislation/Legacy_Regulations": ("MOUUK-0003",),
    "01_Legislation/Other_Relevant_Legislation": ("MOUUK-0004",),
    "03_Procurement_Policy_Notes": ("MOUUK-0005",),
    "04_NPPS_and_Government_Policy": ("MOUUK-0006",),
    "05_Cabinet_Office_Guidance/Plan": ("MOUUK-0007",),
    "05_Cabinet_Office_Guidance/Define": ("MOUUK-0008",),
    "05_Cabinet_Office_Guidance/Procure": ("MOUUK-0009",),
    "05_Cabinet_Office_Guidance/Manage": ("MOUUK-0010",),
}

TAG_MODULES: dict[str, tuple[str, ...]] = {
    "social_value": ("MOUUK-0011",),
    "supplier_selection": ("MOUUK-0013",),
    "exclusion_debarment": ("MOUUK-0014",),
    "transparency": ("MOUUK-0015",),
    "frameworks_dynamic_markets": ("MOUUK-0016", "MOUUK-0017"),
    "contract_management": ("MOUUK-0018",),
    "carbon": ("MOUUK-0019",),
    "security": ("MOUUK-0021",),
    "SME_VCSE": ("MOUUK-0020",),
}

TITLE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "MOUUK-0012": ("TOMs", "Themes Outcomes Measures", "social value"),
    "MOUUK-0020": ("modern slavery", "responsible supply chain"),
    "MOUUK-0022": ("data protection", "UK GDPR", "information governance"),
}

# These modules are evidence infrastructure. They need authoritative PDFs as references
# but do not own a separate legal subject area.
CROSS_CUTTING_MODULES = ("MOUUK-0023", "MOUUK-0024", "MOUUK-0025", "MOUUK-0026")


def route_modules(category: str, tags: Iterable[str], title: str = "") -> tuple[str, ...]:
    result: list[str] = list(CATEGORY_MODULES.get(category, ()))
    tag_set = set(tags)
    for tag, modules in TAG_MODULES.items():
        if tag in tag_set:
            result.extend(modules)

    haystack = title.casefold()
    for module, keywords in TITLE_KEYWORDS.items():
        if any(keyword.casefold() in haystack for keyword in keywords):
            result.append(module)

    # The source/evidence layer is always useful to these four modules.
    result.extend(CROSS_CUTTING_MODULES)
    return tuple(dict.fromkeys(result))


def module_reference_dirs(root: Path, modules: Iterable[str]) -> dict[str, Path]:
    refs: dict[str, Path] = {}
    for code in modules:
        path = root / "modules" / code / "references"
        path.mkdir(parents=True, exist_ok=True)
        refs[code] = path
    return refs
