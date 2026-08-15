import json

import pytest

from faceless_marketing.ledger import CampaignLedger, CampaignRecord, Metric


def record(**overrides):
    data = {
        "campaign_id": "camp-001",
        "asset_id": "asset-001",
        "name": "release-aug",
        "channel": "community",
        "source": "faceless-marketing",
        "destination": "https://example.com/docs?x=1#section",
        "objective": "discoverability",
        "hypothesis": "A technical release note will increase qualified repository visits.",
        "published_at": "2026-08-15T10:00:00+05:00",
    }
    data.update(overrides)
    return CampaignRecord(**data)


def test_json_is_deterministic_and_normalizes_timestamp():
    ledger = CampaignLedger((record(campaign_id="b"), record(campaign_id="a")))
    first = ledger.to_json()
    second = ledger.to_json()
    assert first == second
    payload = json.loads(first)
    assert [item["campaign_id"] for item in payload["campaigns"]] == ["a", "b"]
    assert payload["campaigns"][0]["published_at"] == "2026-08-15T05:00:00Z"


def test_utm_is_derived_not_authoritative_storage():
    result = record().utm_url()
    assert "utm_source=faceless-marketing" in result
    assert "utm_medium=community" in result
    assert "utm_campaign=release-aug" in result
    assert result.endswith("#section")


def test_duplicate_campaign_id_rejected():
    ledger = CampaignLedger((record(),))
    with pytest.raises(ValueError, match="duplicate campaign_id"):
        ledger.add(record())


def test_measured_requires_evidence_and_metric():
    with pytest.raises(ValueError, match="measured campaigns require"):
        record(result_state="measured")
    with pytest.raises(ValueError, match="evidence_source"):
        record(result_state="measured", metrics=(Metric("visits", 10, "analytics"),))


def test_negative_metrics_rejected():
    with pytest.raises(ValueError, match="must not be negative"):
        Metric("visits", -1, "analytics")


def test_naive_timestamp_rejected():
    with pytest.raises(ValueError, match="explicit timezone"):
        record(published_at="2026-08-15T10:00:00")


def test_credentials_and_bad_scheme_rejected():
    with pytest.raises(ValueError, match="credentials"):
        record(destination="https://user:pass@example.com/path")
    with pytest.raises(ValueError, match="absolute http\(s\) URL"):
        record(destination="javascript:alert(1)")


def test_json_round_trip():
    original = CampaignLedger((record(metrics=(Metric("visits", 12, "analytics"),), result_state="measured", evidence_source="analytics-export.json"),))
    restored = CampaignLedger.from_json(original.to_json())
    assert restored.to_json() == original.to_json()


def test_csv_is_stable():
    ledger = CampaignLedger((record(),))
    csv_text = ledger.to_csv()
    assert csv_text.count("\n") == 2
    assert "campaign_id" in csv_text
    assert "camp-001" in csv_text
