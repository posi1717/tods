from __future__ import annotations

from typing import Iterable

# Deterministic routing from collector classification into the 26 MOUUK experts.
# Routing creates SKBUK delivery references; MOUUK never owns the source PDF.
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

    result.extend(CROSS_CUTTING_MODULES)
    return tuple(dict.fromkeys(result))
