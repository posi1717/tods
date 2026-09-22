import re
from typing import Dict, Any

class SKBUKCalibrator:
    def __init__(self):
        self.primary_keywords = ["procurement act 2023", "ppn", "ai regulation", "public contract"]
        self.min_content_length = 150

    def calibrate(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        text = raw_data.get("content", "").lower()
        score = 100
        flags = []

        if len(text) < self.min_content_length:
            score -= 40
            flags.append("CONTENT_TOO_SHORT")

        found_keywords = [kw for kw in self.primary_keywords if kw in text]
        if not found_keywords:
            score -= 50
            flags.append("MISSING_PRIMARY_UK_REGULATORY_KEYWORDS")

        is_passed = score >= 60

        return {
            "is_passed": is_passed,
            "calibration_score": score,
            "detected_keywords": found_keywords,
            "flags": flags,
            "target_mouuk_routing": self._route_to_mouuk(text)
        }

    def _route_to_mouuk(self, text: str) -> str:
        if "procurement act" in text:
            return "MOUUK_01_ProcurementAct"
        elif "ppn" in text:
            return "MOUUK_02_PPN_Compliance"
        elif "ai" in text:
            return "MOUUK_AI_Regulation"
        return "MOUUK_General_Compliance"
