from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from .core import Campaign, build_utm

_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_ALLOWED_RESULTS = {"planned", "published", "measured", "inconclusive"}


def _text(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be a string")
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError(f"{field_name} must not contain control characters")
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} must not be empty")
    return value


def _url(value: str, field_name: str) -> str:
    value = _text(value, field_name)
    parts = urlsplit(value)
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError(f"{field_name} must be an absolute http(s) URL")
    if parts.username is not None or parts.password is not None:
        raise ValueError(f"{field_name} must not contain embedded credentials")
    return value


def _timestamp(value: str) -> str:
    value = _text(value, "published_at")
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("published_at must be ISO-8601") from exc
    if dt.tzinfo is None:
        raise ValueError("published_at must include an explicit timezone")
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class Metric:
    name: str
    value: float
    source: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _text(self.name, "metric.name"))
        if isinstance(self.value, bool) or not isinstance(self.value, (int, float)):
            raise TypeError("metric.value must be numeric")
        if self.value < 0:
            raise ValueError("metric.value must not be negative")
        object.__setattr__(self, "source", _text(self.source, "metric.source"))


@dataclass(frozen=True)
class CampaignRecord:
    campaign_id: str
    asset_id: str
    name: str
    channel: str
    source: str
    destination: str
    objective: str
    hypothesis: str
    published_at: str
    result_state: str = "planned"
    metrics: tuple[Metric, ...] = field(default_factory=tuple)
    evidence_source: str | None = None

    def __post_init__(self) -> None:
        for field_name in ("campaign_id", "asset_id", "name", "channel", "source", "objective", "hypothesis"):
            value = _text(getattr(self, field_name), field_name)
            if field_name in {"campaign_id", "asset_id"} and not _ID_RE.fullmatch(value):
                raise ValueError(f"{field_name} contains unsupported characters")
            object.__setattr__(self, field_name, value)
        object.__setattr__(self, "destination", _url(self.destination, "destination"))
        object.__setattr__(self, "published_at", _timestamp(self.published_at))
        if self.result_state not in _ALLOWED_RESULTS:
            raise ValueError(f"result_state must be one of {sorted(_ALLOWED_RESULTS)}")
        metrics = tuple(self.metrics)
        if any(not isinstance(m, Metric) for m in metrics):
            raise TypeError("metrics must contain Metric objects")
        if len({m.name for m in metrics}) != len(metrics):
            raise ValueError("metric names must be unique within a campaign")
        if self.result_state == "measured" and not metrics:
            raise ValueError("measured campaigns require at least one recorded metric")
        if metrics and not self.evidence_source:
            raise ValueError("recorded metrics require an evidence_source")
        if self.evidence_source is not None:
            object.__setattr__(self, "evidence_source", _text(self.evidence_source, "evidence_source"))

    def utm_url(self) -> str:
        campaign = Campaign(self.name, self.channel, self.objective, self.source)
        return build_utm(self.destination, campaign)

    def as_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["metrics"] = [asdict(metric) for metric in self.metrics]
        data["utm_url"] = self.utm_url()
        return data


class CampaignLedger:
    """In-memory, deterministic campaign ledger with JSON/CSV persistence."""

    def __init__(self, records: tuple[CampaignRecord, ...] = ()) -> None:
        self._records: dict[str, CampaignRecord] = {}
        for record in records:
            self.add(record)

    def add(self, record: CampaignRecord) -> None:
        if record.campaign_id in self._records:
            raise ValueError(f"duplicate campaign_id: {record.campaign_id}")
        self._records[record.campaign_id] = record

    def records(self) -> tuple[CampaignRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))

    def to_json(self) -> str:
        payload = {"version": 1, "campaigns": [r.as_dict() for r in self.records()]}
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"

    def to_csv(self) -> str:
        fields = ["campaign_id", "asset_id", "name", "channel", "source", "destination", "objective", "hypothesis", "published_at", "result_state", "evidence_source", "utm_url", "metrics"]
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for record in self.records():
            row = record.as_dict()
            row["metrics"] = json.dumps(row["metrics"], sort_keys=True, separators=(",", ":"))
            writer.writerow({field: row.get(field, "") for field in fields})
        return out.getvalue()

    def save_json(self, path: Path) -> None:
        path.write_text(self.to_json(), encoding="utf-8")

    def save_csv(self, path: Path) -> None:
        path.write_text(self.to_csv(), encoding="utf-8", newline="")

    @classmethod
    def from_json(cls, text: str) -> "CampaignLedger":
        payload = json.loads(text)
        if not isinstance(payload, dict) or payload.get("version") != 1 or not isinstance(payload.get("campaigns"), list):
            raise ValueError("unsupported or malformed ledger JSON")
        records = []
        for item in payload["campaigns"]:
            if not isinstance(item, dict):
                raise ValueError("campaign entries must be objects")
            metrics = tuple(Metric(**metric) for metric in item.pop("metrics", []))
            item.pop("utm_url", None)
            records.append(CampaignRecord(metrics=metrics, **item))
        return cls(tuple(records))
