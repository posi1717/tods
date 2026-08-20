"""Independent reasoning worker for Other Relevant Legislation."""

from pathlib import Path

from ..base import ReasoningWorker


class OtherRelevantLegislationWorker(ReasoningWorker):
    pass


def create_worker() -> OtherRelevantLegislationWorker:
    return OtherRelevantLegislationWorker(Path(__file__).parent)
