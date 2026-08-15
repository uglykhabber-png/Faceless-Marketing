from faceless_marketing.attribution import attribute_observed_metric
from faceless_marketing.ledger import CampaignLedger, CampaignRecord, Metric


def record(**overrides):
    data = dict(
        campaign_id="camp-001",
        asset_id="asset-001",
        name="release",
        channel="community",
        source="faceless-marketing",
        destination="https://example.com/docs",
        objective="discoverability",
        hypothesis="The release documentation improves qualified discovery.",
        published_at="2026-08-15T00:00:00Z",
        result_state="measured",
        metrics=(Metric("visits", 12, "analytics"),),
        evidence_source="analytics-export.json",
    )
    data.update(overrides)
    return CampaignRecord(**data)


def test_explicit_metric_is_observed_not_causal():
    ledger = CampaignLedger((record(),))
    result = attribute_observed_metric(ledger, "camp-001", "visits")
    assert result.status == "observed"
    assert result.value == 12.0
    assert result.evidence_source == "analytics-export.json"


def test_unknown_campaign_is_unattributed():
    result = attribute_observed_metric(CampaignLedger(), "missing", "visits")
    assert result.status == "unattributed"
    assert result.value is None


def test_unknown_metric_is_unattributed():
    result = attribute_observed_metric(CampaignLedger((record(),)), "camp-001", "conversions")
    assert result.status == "unattributed"
    assert result.value is None
