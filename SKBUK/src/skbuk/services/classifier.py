from urllib.parse import urlparse
from skbuk.taxonomy.official import OfficialFamily


def classify(url: str, landing_url: str, title: str) -> OfficialFamily:
    path = urlparse(url).path.lower()
    landing = urlparse(landing_url).path.lower()
    if "/ukpga/" in path:
        return OfficialFamily.PRIMARY_LEGISLATION
    if "/uksi/" in path:
        return OfficialFamily.SECONDARY_LEGISLATION
    if "procurement-policy-notes" in landing or "ppn" in title.lower():
        return OfficialFamily.POLICY_NOTES
    if "supplier" in landing or "supplier" in title.lower():
        return OfficialFamily.SUPPLIER_GUIDANCE
    if "guidance" in landing or "guidance" in title.lower():
        return OfficialFamily.GUIDANCE
    return OfficialFamily.MISC
