from dataclasses import dataclass, asdict
from urllib.parse import urlencode

@dataclass(frozen=True)
class Campaign:
    name: str
    channel: str
    objective: str
    source: str = "faceless-marketing"

def build_utm(base_url: str, campaign: Campaign) -> str:
    if not base_url.startswith(("http://", "https://")):
        raise ValueError("base_url must use http:// or https://")
    params = {
        "utm_source": campaign.source,
        "utm_medium": campaign.channel,
        "utm_campaign": campaign.name,
    }
    separator = "&" if "?" in base_url else "?"
    return base_url + separator + urlencode(params)

def export_campaign(campaign: Campaign) -> dict:
    return asdict(campaign)
