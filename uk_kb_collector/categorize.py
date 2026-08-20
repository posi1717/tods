from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class Classification:
    category: str
    publisher: str
    document_type: str
    legislation_or_policy_reference: str
    tags: list[str]
    needs_review: bool
    notes: str


def _match(text: str, patterns: list[str]) -> bool:
    low = text.lower()
    return any(p.lower() in low for p in patterns)


def classify(url: str, landing_title: str, pdf_meta: dict[str, str], hint: str, tags_config: dict) -> Classification:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    text = " ".join([landing_title, pdf_meta.get("title", ""), pdf_meta.get("subject", ""), pdf_meta.get("text", ""), url])
    low = text.lower()

    publisher = "Cabinet Office" if "cabinetoffice" in host or "cabinet office" in low else "unknown-publisher"
    if "gov.uk" in host:
        publisher = publisher if publisher != "unknown-publisher" else "UK Government"
    elif "legislation.gov.uk" in host:
        publisher = "UK Parliament / legislation.gov.uk"

    # Source hints take precedence over incidental references in a PDF.
    if hint == "procurement_policy_notes":
        category = "03_Procurement_Policy_Notes"; ref = ""; dtype = "policy_note"
    elif hint == "government_policy":
        category = "04_NPPS_and_Government_Policy"; ref = ""; dtype = "government_policy"
    elif hint == "statutory_guidance":
        phase = next((p for p in ["plan", "define", "procure", "manage"] if f"{p} phase" in low or f"/{p}-phase" in low), "")
        category = f"05_Cabinet_Office_Guidance/{phase.title()}" if phase else "02_Statutory_Guidance"
        ref = "Procurement Act 2023"; dtype = "statutory_guidance"
    elif hint == "legislation" or "Procurement Act 2023" in text:
        category = "01_Legislation/Procurement_Act_2023"; ref = "Procurement Act 2023"; dtype = "legislation"
    elif hint == "procurement_regulations_2024" or "Procurement Regulations 2024" in text:
        category = "01_Legislation/Procurement_Regulations_2024"; ref = "Procurement Regulations 2024"; dtype = "secondary_legislation"
    elif hint == "legacy_regulations" or any(x in text for x in ["Public Contracts Regulations 2015", "Utilities Contracts Regulations 2016", "Concession Contracts Regulations 2016", "Defence and Security Public Contracts Regulations 2011"]):
        category = "01_Legislation/Legacy_Regulations"
        ref = next((x for x in ["Public Contracts Regulations 2015", "Utilities Contracts Regulations 2016", "Concession Contracts Regulations 2016", "Defence and Security Public Contracts Regulations 2011"] if x in text), "legacy procurement regulations")
        dtype = "legacy_secondary_legislation"
    elif hint == "other_legislation" or "Public Services (Social Value) Act 2012" in text:
        category = "01_Legislation/Other_Relevant_Legislation"; ref = "Public Services (Social Value) Act 2012"; dtype = "legislation"
    elif "National Procurement Policy Statement" in text or "NPPS" in text:
        category = "04_NPPS_and_Government_Policy"; ref = "National Procurement Policy Statement"; dtype = "government_policy"
    elif "procurement policy note" in low or re.search(r"\bPPN\b", text, re.I):
        category = "03_Procurement_Policy_Notes"; ref = ""; dtype = "policy_note"
    elif "playbook" in low or "framework" in low or "standard" in low:
        category = "06_Frameworks_Standards_Playbooks"; ref = ""; dtype = "framework_or_playbook"
    elif "template" in low or "model document" in low:
        category = "07_Templates_and_Model_Documents"; ref = ""; dtype = "template_model_document"
    elif "procurement policy" in low:
        category = "04_NPPS_and_Government_Policy"; ref = ""; dtype = "government_policy"
    else:
        category = "00_Inbox"; ref = ""; dtype = "unknown"

    tags: list[str] = []
    for tag, patterns in tags_config.items():
        if _match(text, patterns):
            tags.append(tag)

    needs_review = category == "00_Inbox"
    note = "NEEDS_REVIEW" if needs_review else ""
    return Classification(category, publisher, dtype, ref, sorted(tags), needs_review, note)
