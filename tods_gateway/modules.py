"""
Registry and routing metadata for the 34 MOUUK specialist modules.

The manifest is declarative: individual specialist logic can evolve without
changing the gateway contract or bypassing calibration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import AuthorityLevel


@dataclass(frozen=True)
class ModuleDefinition:
    module_id: str
    name: str
    purpose: str
    minimum_authorities: tuple[AuthorityLevel, ...]
    depends_on: tuple[str, ...] = ()


CORE_AUTHORITIES = (
    AuthorityLevel.PRIMARY_LAW,
    AuthorityLevel.SECONDARY_LEGISLATION,
    AuthorityLevel.OFFICIAL_GUIDANCE,
    AuthorityLevel.POLICY_NOTICE,
    AuthorityLevel.OFFICIAL_PLATFORM,
)

MOUUK_MODULES: tuple[ModuleDefinition, ...] = (
    ModuleDefinition("MOUUK-0001", "Procurement Act 2023", "Interpret requirements under the Procurement Act 2023.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0002", "Procurement Regulations 2024", "Interpret requirements under the Procurement Regulations 2024.", CORE_AUTHORITIES, ("MOUUK-0001",)),
    ModuleDefinition("MOUUK-0003", "Transitional Regulations", "Determine applicability of transitional procurement rules.", CORE_AUTHORITIES, ("MOUUK-0001", "MOUUK-0002")),
    ModuleDefinition("MOUUK-0004", "Procurement Lifecycle", "Map guidance across plan, define, procure and manage stages.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0005", "Notices and Transparency", "Assess notices, publication and transparency duties.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0006", "Tender Procedures", "Assess procedure selection and tender-process requirements.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0007", "Mandatory Requirements", "Identify mandatory bidder and authority requirements.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0008", "Exclusions and Debarment", "Assess exclusion and debarment rules.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0009", "Selection Criteria", "Assess selection-stage requirements and proportionality.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0010", "Award Criteria", "Assess award criteria, scoring and evaluation conditions.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0011", "Evaluation Governance", "Assess evaluator controls, moderation and auditability.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0012", "Clarifications", "Assess clarification processes and equal-treatment controls.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0013", "Conflicts of Interest", "Assess conflict identification, mitigation and record keeping.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0014", "SME and VCSE Participation", "Assess SME and VCSE accessibility requirements.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0015", "Social Value", "Assess social-value requirements and policy alignment.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0016", "Carbon and Net Zero", "Assess carbon, net-zero and sustainability requirements.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0017", "Prompt Payment", "Assess prompt-payment requirements and evidence.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0018", "Modern Slavery", "Assess modern-slavery declarations and supply-chain obligations.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0019", "Cyber and Information Security", "Assess security, data-protection and information-assurance requirements.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0020", "Frameworks and Dynamic Markets", "Assess frameworks, dynamic markets and call-off requirements.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0021", "Contract Terms", "Assess contract terms, KPIs, remedies and governance.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0022", "Contract Modifications", "Assess modification controls and notice obligations.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0023", "Contract Management", "Assess delivery, performance and supplier-management controls.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0024", "Remedies and Challenges", "Assess remedies, standstill and challenge risks.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0025", "Data and Records", "Assess procurement records, retention and evidence obligations.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0026", "Public Procurement Policy Notes", "Map relevant PPN requirements to procurement activity.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0027", "Pre-market Engagement", "Assess compliant preliminary market engagement.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0028", "Direct Award", "Assess lawful direct-award routes and required evidence.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0029", "Below-threshold Procurement", "Assess below-threshold process and transparency requirements.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0030", "Emergency Procurement", "Assess urgency and emergency procurement conditions.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0031", "International Trade", "Assess treaty and international procurement obligations.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0032", "Accessibility and Equality", "Assess accessibility and equality considerations.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0033", "Financial Standing", "Assess financial checks, insurance and economic capacity.", CORE_AUTHORITIES),
    ModuleDefinition("MOUUK-0034", "Evidence and Provenance", "Validate provenance, versioning and audit-trail completeness.", CORE_AUTHORITIES),
)

MODULES_BY_ID = {module.module_id: module for module in MOUUK_MODULES}


def get_module(module_id: str) -> ModuleDefinition:
    try:
        return MODULES_BY_ID[module_id]
    except KeyError as error:
        raise ValueError(f"Unknown MOUUK module: {module_id}") from error


def list_modules() -> Iterable[ModuleDefinition]:
    return MOUUK_MODULES
