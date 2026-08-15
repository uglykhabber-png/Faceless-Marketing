from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

_ALLOWED_SEVERITIES = {"info", "low", "medium", "high", "critical"}


def _validate_text(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    value = value.strip()
    if not value:
        raise ValueError(f"{field} must not be empty")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{field} must not contain control characters")
    return value


def _validate_severity(value: str) -> str:
    value = _validate_text(value, "severity").lower()
    if value not in _ALLOWED_SEVERITIES:
        raise ValueError(f"unsupported severity: {value}")
    return value


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
