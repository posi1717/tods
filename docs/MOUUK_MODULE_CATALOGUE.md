# UKKB MOUUK — 34 Expert Knowledge Modules



MOUUK is the expert-knowledge layer. The 34 modules do **not** own source PDFs. SKBUK is the source-of-truth document store and governance layer; MOUUK receives references/manifests from SKBUK.

## Folder / knowledge tree

```text
UKKB/
├── SKBUK/                                  # Knowledge supply + governance layer
│   ├── documents/                          # SOURCE OF TRUTH: original PDFs + metadata
│   │   └── <document_id>/
│   │       ├── original.pdf
│   │       └── metadata.json               # source_url, publisher, version, hash, etc.
│   ├── delivery/
│   │   └── MOUUK/
│   │       ├── MOUUK-0001.json
│   │       ├── MOUUK-0002.json
│   │       ├── ...
│   │       └── MOUUK-0034.json
│   ├── audit/
│   │   └── events.jsonl
│   └── source_registry.yaml                # approved authoritative sources
│
├── MOUUK/                                  # 34 expert knowledge modules
│   ├── MOUUK-0001/ ... MOUUK-0034/
│   │   ├── manifest.yaml                   # identity + capabilities
│   │   ├── rules/                           # specialist rules/taxonomy
│   │   └── references/                     # DELIVERY REFERENCES ONLY; not source-of-truth
│   │
│   └── ...
│
├── uk_kb_collector/                        # ingestion service
│   ├── discover.py
│   ├── collector.py
│   ├── pdf.py
│   ├── registry.py
│   ├── skbuk.py
│   └── modules.yaml
│
└── docs/
    └── MOUUK_MODULE_CATALOGUE.md
```

> Git does not persist empty directories. Runtime creates module/reference directories when a document is delivered.

## Module catalogue

| Code       | Module                                      | Meaning / responsibility                                                           | Key properties                                                                | Primary evidence                                  |
| ---------- | ------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------- |
| MOUUK-0001 | Procurement Act 2023                        | Expert on the Procurement Act 2023 statutory framework                             | statutory interpretation, duties, procedures, thresholds, notices             | legislation.gov.uk + official gov.uk guidance     |
| MOUUK-0002 | Procurement Regulations 2024                | Expert on regulations made under the Procurement Act                               | regulatory requirements, prescribed information, notices, procedures          | legislation.gov.uk + gov.uk                       |
| MOUUK-0003 | Legacy Procurement Regulations              | Expert on pre-2024 procurement regimes and transition                              | PCR 2015, UCR 2016, CCR 2016, DSPCR 2011, transitional context                | legislation.gov.uk                                |
| MOUUK-0004 | Other Relevant Legislation                  | Expert on legislation that affects procurement but is not the core Procurement Act | cross-law applicability, statutory constraints, subject-specific legislation  | legislation.gov.uk + official department guidance |
| MOUUK-0005 | Procurement Policy Notes                    | Expert on Cabinet Office PPN requirements and policy notices                       | PPN applicability, mandatory/recommended actions, effective dates             | gov.uk / Cabinet Office                           |
| MOUUK-0006 | National Procurement Policy Statement       | Expert on NPPS priorities and applicability                                        | national priorities, contracting-authority duties, policy alignment           | gov.uk / Cabinet Office                           |
| MOUUK-0007 | Plan                                        | Expert for procurement planning and pre-market strategy                            | pipeline, objectives, governance, market strategy, route planning             | official government guidance / buyer policy       |
| MOUUK-0008 | Define                                      | Expert for requirements and specification definition                               | outcomes, scope, requirements, evaluation design, market engagement           | official guidance / buyer documentation           |
| MOUUK-0009 | Procure                                     | Expert for the procurement execution stage                                         | procedures, tendering, evaluation, award, notices, compliance                 | legislation + official guidance                   |
| MOUUK-0010 | Manage                                      | Expert for post-award contract management                                          | performance, governance, change, payment, termination                         | official contract-management guidance             |
| MOUUK-0011 | Social Value                                | Expert on social-value procurement policy                                          | social value objectives, evaluation, commitments, delivery                    | gov.uk + official policy                          |
| MOUUK-0012 | TOMs                                        | Specialist child module of Social Value for Themes, Outcomes and Measures          | TOMs mapping, measurement, metrics, social-value evidence                     | official buyer/framework materials                |
| MOUUK-0013 | Supplier Selection                          | Expert on supplier qualification and conditions of participation                   | SQ, conditions, selection criteria, financial/technical capability            | legislation + official guidance                   |
| MOUUK-0014 | Exclusion and Debarment                     | Expert on supplier exclusion and debarment                                         | mandatory/discretionary grounds, debarment list, due diligence                | legislation + Cabinet Office guidance             |
| MOUUK-0015 | Transparency and Procurement Data           | Expert on transparency obligations and procurement data                            | notices, publication, Contracts Finder/CDP data, disclosure                   | legislation + official platforms                  |
| MOUUK-0016 | Framework Agreements                        | Expert on framework procurement structures                                         | framework design, call-offs, award mechanisms, rules                          | legislation + official guidance                   |
| MOUUK-0017 | Dynamic Markets                             | Expert on Dynamic Markets                                                          | admission, operation, competition, supplier access                            | legislation + official guidance                   |
| MOUUK-0018 | Contract Management and Open Book           | Expert on contract performance and open-book management                            | KPIs, payment, open book, modification, governance                            | official guidance + contract policy               |
| MOUUK-0019 | Sustainability and Carbon                   | Expert on environmental and carbon requirements                                    | net zero, carbon reduction, environmental criteria, reporting                 | official government policy/guidance               |
| MOUUK-0020 | Modern Slavery and Responsible Supply Chain | Expert on modern slavery and responsible sourcing                                  | due diligence, supply-chain risk, reporting, remediation                      | legislation + gov.uk guidance                     |
| MOUUK-0021 | Security and National Security              | Expert on security-sensitive procurement                                           | national security, security controls, supplier risk, classified context       | legislation + official security guidance          |
| MOUUK-0022 | Data Protection and Information Governance  | Expert on data protection and information governance in procurement                | UK GDPR, DPA 2018, DPIA, information governance, records                      | legislation + ICO/official guidance               |
| MOUUK-0023 | Source Authority                            | Governance expert that determines whether evidence is authoritative                | source tier, publisher, jurisdiction, authority status, allow/reject          | SKBUK Source Registry + official domains          |
| MOUUK-0024 | Temporal and Version Intelligence           | Governance expert for document currency                                            | publication/update dates, supersession, version comparison, effective periods | SKBUK provenance/version metadata                 |
| MOUUK-0025 | Cross-Governance Relationships              | Expert on relationships between laws, policies, guidance and modules               | dependencies, conflicts, applicability, cross-module links                    | SKBUK provenance + official sources               |
| MOUUK-0026 | Evidence and Provenance                     | Expert on traceability of every knowledge claim                                    | document ID, source URL, hash, citation chain, evidence status                | SKBUK document metadata + audit trail             |
| MOUUK-0027 | Procedures and Award Criteria               | Expert on procurement procedures and award criteria                                | procedure selection, award criteria, evaluation design                        | legislation + official guidance                   |
| MOUUK-0028 | Notices, Standstill and Remedies            | Expert on award notices, standstill and procurement remedies                       | notices, challenge periods, remedies, court process                           | legislation + official guidance                   |
| MOUUK-0029 | Below-threshold and Covered Procurement     | Expert on below-threshold and covered procurement                                  | coverage, thresholds, procedures, transparency                                | legislation + official guidance                   |
| MOUUK-0030 | Conflicts of Interest                       | Expert on conflicts of interest in procurement                                     | identification, mitigation, declarations, records                             | legislation + official guidance                   |
| MOUUK-0031 | SME, VCSE and Reserved Contracts            | Expert on SME, VCSE and reserved-contract policy                                   | access, reservation, participation, policy outcomes                           | legislation + official guidance                   |
| MOUUK-0032 | Devolved and Sector Regimes                 | Expert on devolved administrations and sector-specific regimes                     | jurisdiction, utilities, defence, sector rules                                | legislation + official guidance                   |
| MOUUK-0033 | Economic and Financial Standing             | Expert on supplier economic and financial standing                                 | financial assessment, insurance, evidence, proportionality                    | legislation + official guidance                   |
| MOUUK-0034 | Insurance and Mandatory Policies            | Expert on insurance and mandatory procurement policies                             | insurance requirements, policy compliance, evidence                           | legislation + official guidance                   |

## Processing boundary

MOUUK receives authoritative references first. The current ingestion phase is **raw PDF only**:

`discover -> validate -> store in SKBUK -> provenance/audit -> deliver reference manifest -> MOUUK`

Only after the raw corpus is accepted should the next phase run:

`PDF -> extract -> normalize -> chunk -> embed -> retrieval`

No MOUUK module may silently replace, modify, or become the canonical owner of the original PDF.
