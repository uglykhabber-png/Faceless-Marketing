import pytest
from faceless_marketing.core import Campaign, build_utm

def test_utm_build():
    c = Campaign("launch", "github", "discoverability")
    out = build_utm("https://example.com/project", c)
    assert "utm_source=faceless-marketing" in out
    assert "utm_medium=github" in out
    assert "utm_campaign=launch" in out

def test_existing_query():
    c = Campaign("x", "docs", "education")
    out = build_utm("https://example.com/?a=1", c)
    assert "?a=1&" in out

def test_invalid_scheme():
    with pytest.raises(ValueError):
        build_utm("javascript:alert(1)", Campaign("x","web","x"))
