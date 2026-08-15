import pytest
from faceless_marketing.core import Campaign, build_utm
from faceless_marketing.evidence import Evidence, Finding


@pytest.mark.parametrize(
    "url",
    [
        "",
        "example.com",
        "file:///tmp/a",
        "javascript:1",
        "https:///missing-host",
        "https://user:pass@example.com",
        "https://example.com/\nunsafe",
    ],
)
def test_rejects_unsafe_or_invalid_urls(url):
    with pytest.raises(ValueError):
        build_utm(url, Campaign("x", "web", "x"))


def test_deterministic_output():
    c = Campaign("same", "github", "x")
    assert build_utm("https://example.com", c) == build_utm("https://example.com", c)


def test_existing_utm_parameters_do_not_accumulate():
    c = Campaign("second", "github", "x")
    out = build_utm("https://example.com?a=1&utm_source=first&utm_campaign=first", c)
    assert out.count("utm_source=") == 1
    assert out.count("utm_medium=") == 1
    assert out.count("utm_campaign=") == 1
    assert "utm_campaign=second" in out


def test_campaign_rejects_control_characters():
    with pytest.raises(ValueError):
        Campaign("x\x00y", "github", "x")


def test_evidence_rejects_unknown_severity():
    with pytest.raises(ValueError):
        Evidence("RULE", "README.md", "description", "banana")


def test_finding_requires_evidence_instances():
    with pytest.raises(TypeError):
        Finding("RULE", "Title", "low", "message", "fix", evidence=("not evidence",))


def test_finding_json_shape_is_stable():
    e = Evidence("RULE", "README.md", "description", "low")
    f = Finding("RULE", "Title", "low", "message", "fix", evidence=(e,))
    assert list(f.as_dict()) == ["rule_id", "title", "severity", "message", "remediation", "evidence"]
    assert f.as_dict()["evidence"][0]["severity"] == "low"
