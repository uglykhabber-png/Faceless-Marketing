import pytest
from faceless_marketing.core import Campaign, build_utm

@pytest.mark.parametrize("url", ["", "example.com", "file:///tmp/a", "javascript:1"])
def test_rejects_unsafe_or_invalid_urls(url):
    with pytest.raises(ValueError):
        build_utm(url, Campaign("x","web","x"))

def test_deterministic_output():
    c = Campaign("same", "github", "x")
    assert build_utm("https://example.com", c) == build_utm("https://example.com", c)
