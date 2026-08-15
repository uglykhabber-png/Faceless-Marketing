import pytest
from faceless_marketing.core import Campaign, build_utm


def test_utm_build():
    c = Campaign("launch", "github", "discoverability")
    out = build_utm("https://example.com/project", c)
    assert "utm_source=faceless-marketing" in out
    assert "utm_medium=github" in out
    assert "utm_campaign=launch" in out


def test_existing_query_and_fragment_are_preserved():
    c = Campaign("x", "docs", "education")
    out = build_utm("https://example.com/?a=1#section", c)
    assert "a=1" in out
    assert out.endswith("#section")


def test_existing_utm_values_are_replaced_not_duplicated():
    c = Campaign("new", "docs", "education")
    out = build_utm(
        "https://example.com/?utm_source=old&utm_medium=old&utm_campaign=old&a=1",
        c,
    )
    assert out.count("utm_source=") == 1
    assert out.count("utm_medium=") == 1
    assert out.count("utm_campaign=") == 1
    assert "utm_campaign=new" in out
    assert "a=1" in out


def test_invalid_scheme():
    with pytest.raises(ValueError):
        build_utm("javascript:alert(1)", Campaign("x", "web", "x"))


def test_missing_hostname():
    with pytest.raises(ValueError):
        build_utm("https:///missing-host", Campaign("x", "web", "x"))


def test_embedded_credentials_are_rejected():
    with pytest.raises(ValueError):
        build_utm("https://user:pass@example.com", Campaign("x", "web", "x"))


def test_empty_campaign_fields_are_rejected():
    with pytest.raises(ValueError):
        Campaign("", "web", "x")


def test_control_characters_are_rejected():
    with pytest.raises(ValueError):
        Campaign("launch\n", "web", "x")
