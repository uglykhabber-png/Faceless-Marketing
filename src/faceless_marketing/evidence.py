from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

_ALLOWED_SEVERITIES = {"info", "low", "medium", "high", "critical"}
_ALLOWED_STATES = {"observed", "derived", "estimated", "inferred", "unknown"}


def _validate_text(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{field} must not contain control characters")
    value = value.strip()
    if not value:
        raise ValueError(f"{field} must not be empty")
    return value


def _validate_severity(value: str) -> str:
    value = _validate_text(value, "severity").lower()
    if value not in _ALLOWED_SEVERITIES:
        raise ValueError(f"unsupported severity: {value}")
    return value


def _validate_state(value: str) -> str:
    value = _validate_text(value, "state").lower()
    if value not in _ALLOWED_STATES:
        raise ValueError(f"unsupported evidence state: {value}")
    return value


def _validate_timestamp(value: str, field: str = "observed_at") -> str:
    value = _validate_text(value, field)
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{field} must include an explicit timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class Evidence:
    rule_id: str
    source: str
    description: str
    severity: str = "info"

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", _validate_text(self.rule_id, "rule_id"))
        object.__setattr__(self, "source", _validate_text(self.source, "source"))
        object.__setattr__(self, "description", _validate_text(self.description, "description"))
        object.__setattr__(self, "severity", _validate_severity(self.severity))

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    source: str
    description: str
    state: str = "observed"
    observed_at: str | None = None
    confidence: float = 1.0

    def __post_init__(self) -> None:
        for name in ("evidence_id", "source", "description"):
            object.__setattr__(self, name, _validate_text(getattr(self, name), name))
        object.__setattr__(self, "state", _validate_state(self.state))
        if self.observed_at is not None:
            object.__setattr__(self, "observed_at", _validate_timestamp(self.observed_at))
        if isinstance(self.confidence, bool) or not isinstance(self.confidence, (int, float)):
            raise TypeError("confidence must be numeric")
        if not 0.0 <= float(self.confidence) <= 1.0:
            raise ValueError("confidence must be between 0 and 1")

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["confidence"] = float(self.confidence)
        return data


@dataclass(frozen=True)
class Finding:
    rule_id: str
    title: str
    severity: str
    message: str
    remediation: str
    evidence: tuple[Evidence, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "rule_id", _validate_text(self.rule_id, "rule_id"))
        object.__setattr__(self, "title", _validate_text(self.title, "title"))
        object.__setattr__(self, "severity", _validate_severity(self.severity))
        object.__setattr__(self, "message", _validate_text(self.message, "message"))
        object.__setattr__(self, "remediation", _validate_text(self.remediation, "remediation"))
        if not isinstance(self.evidence, tuple):
            raise TypeError("evidence must be a tuple")
        if not all(isinstance(item, Evidence) for item in self.evidence):
            raise TypeError("evidence items must be Evidence instances")

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "title": self.title,
            "severity": self.severity,
            "message": self.message,
            "remediation": self.remediation,
            "evidence": [item.as_dict() for item in self.evidence],
        }
