from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Recommendation:
    recommendation_id: str
    title: str
    action: str
    priority: float
    evidence_level: str
    rationale: str
    status: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def prioritize(
    *,
    recommendation_id: str,
    title: str,
    action: str,
    expected_value: float,
    evidence: float,
    reach: float = 1.0,
    effort: float = 1.0,
    risk: float = 1.0,
    confidence: float = 1.0,
) -> Recommendation:
    values = {"expected_value": expected_value, "evidence": evidence, "reach": reach, "effort": effort, "risk": risk, "confidence": confidence}
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values.values()):
        raise TypeError("decision inputs must be numeric")
    if expected_value < 0 or evidence < 0 or reach < 0 or effort <= 0 or risk <= 0 or not 0 <= confidence <= 1:
        raise ValueError("invalid decision inputs")
    priority = (evidence * expected_value * reach * confidence) / (effort * risk)
    if evidence < 0.25 or confidence < 0.25:
        status = "INSUFFICIENT_EVIDENCE"
        evidence_level = "low"
    elif priority >= 10:
        status = "DO_NOW"
        evidence_level = "high"
    elif priority >= 3:
        status = "DO_NEXT"
        evidence_level = "medium"
    elif priority > 0:
        status = "TEST"
        evidence_level = "medium"
    else:
        status = "DEFER"
        evidence_level = "low"
    return Recommendation(recommendation_id, title.strip(), action.strip(), round(priority, 4), evidence_level, "Priority is evidence-weighted expected value divided by effort and risk.", status)
