from enum import StrEnum


class OfficialFamily(StrEnum):
    PRIMARY_LEGISLATION = "primary-legislation"
    SECONDARY_LEGISLATION = "secondary-legislation"
    GUIDANCE = "guidance"
    POLICY_NOTES = "policy-notes"
    SUPPLIER_GUIDANCE = "supplier-guidance"
    EXPLANATORY_NOTES = "explanatory-notes"
    MISC = "misc"
