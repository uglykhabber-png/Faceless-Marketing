from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Evidence:
    rule_id: str
    source: str
    description: str
    severity: str = "info"

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

    def as_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["evidence"] = [item.as_dict() for item in self.evidence]
        return result
