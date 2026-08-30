from pathlib import Path
from skbuk.utils.filenames import ensure_relative

OFFICIAL_BUCKET = "tod-official"
BIDDER_BUCKET = "tod-bidder"
TENDER_BUCKET = "tod-tenders"
EXPORT_BUCKET = "tod-exports"


def official_path(relative_path: str) -> str:
    return ensure_relative(relative_path, "01_OFFICIAL_SOURCES/")


def bidder_path(organisation_id: str, category: str, filename: str) -> str:
    if not category.startswith("B"):
        raise ValueError("bidder evidence category must be B01-B10")
    return f"02_BIDDER_EVIDENCE/{organisation_id}/{category}/{filename}"


def tender_path(tender_id: str, section: str, filename: str) -> str:
    allowed = {"ITT", "SPECIFICATION", "PRICING_SCHEDULE", "EVALUATION_CRITERIA", "TERMS_AND_CONDITIONS", "CLARIFICATIONS"}
    if section not in allowed:
        raise ValueError("unsupported tender pack section")
    return f"03_TENDER_WORKSPACES/{tender_id}/01_BUYER_PACK/{section}/{filename}"


def write_immutable(root: Path, relative_path: str, content: bytes) -> Path:
    target = root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.read_bytes() != content:
            raise FileExistsError("immutable storage path already contains different content")
        return target
    target.write_bytes(content)
    return target
