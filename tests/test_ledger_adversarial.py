import pytest

from faceless_marketing.ledger import CampaignLedger, CampaignRecord, Metric


def base():
    return dict(
        campaign_id="safe-001",
        asset_id="asset-001",
        name="release",
        channel="community",
        source="faceless-marketing",
        destination="https://example.com/docs",
        objective="discoverability",
        hypothesis="The documented release path will improve qualified discovery.",
        published_at="2026-08-15T00:00:00Z",
    )


def test_control_characters_rejected():
    with pytest.raises(ValueError):
        CampaignRecord(**{**base(), "hypothesis": "bad\nclaim"})


def test_id_path_traversal_rejected():
    with pytest.raises(ValueError):
        CampaignRecord(**{**base(), "campaign_id": "../secret"})


def test_duplicate_metric_names_rejected():
    metrics = (Metric("visits", 1, "analytics"), Metric("visits", 2, "analytics"))
    with pytest.raises(ValueError, match="metric names"):
        CampaignRecord(**{**base(), "metrics": metrics, "evidence_source": "export.json"})


def test_metrics_without_evidence_rejected():
    with pytest.raises(ValueError, match="evidence_source"):
        CampaignRecord(**{**base(), "metrics": (Metric("visits", 1, "analytics"),)})


def test_unknown_result_state_rejected():
    with pytest.raises(ValueError, match="result_state"):
        CampaignRecord(**{**base(), "result_state": "converted"})


def test_json_rejects_wrong_version():
    with pytest.raises(ValueError, match="unsupported"):
        CampaignLedger.from_json('{"version": 99, "campaigns": []}')


def test_json_rejects_non_object_campaign():
    with pytest.raises(ValueError, match="objects"):
        CampaignLedger.from_json('{"version": 1, "campaigns": [1]}')


def test_non_numeric_metric_rejected():
    with pytest.raises(TypeError, match="numeric"):
        Metric("visits", "100", "analytics")


def test_boolean_metric_rejected():
    with pytest.raises(TypeError, match="numeric"):
        Metric("visits", True, "analytics")
