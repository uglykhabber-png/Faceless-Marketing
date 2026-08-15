from __future__ import annotations

from dataclasses import dataclass

from .ledger import CampaignLedger


@dataclass(frozen=True)
class AttributionResult:
    campaign_id: str
    metric_name: str
    value: float | None
    evidence_source: str | None
    status: str


def attribute_observed_metric(ledger: CampaignLedger, campaign_id: str, metric_name: str) -> AttributionResult:
    """Attribute an explicitly recorded observation to a campaign.

    This function never calculates causal lift, conversion probability, ROI, or
    incremental growth. It only answers whether a named metric was explicitly
    recorded for the named campaign and whether its evidence provenance exists.
    """
    campaign_id = campaign_id.strip()
    metric_name = metric_name.strip()
    if not campaign_id or not metric_name:
        raise ValueError("campaign_id and metric_name must be non-empty")

    record = next((item for item in ledger.records() if item.campaign_id == campaign_id), None)
    if record is None:
        return AttributionResult(campaign_id, metric_name, None, None, "unattributed")

    metric = next((item for item in record.metrics if item.name == metric_name), None)
    if metric is None or not record.evidence_source:
        return AttributionResult(campaign_id, metric_name, None, record.evidence_source, "unattributed")

    return AttributionResult(campaign_id, metric_name, float(metric.value), record.evidence_source, "observed")
