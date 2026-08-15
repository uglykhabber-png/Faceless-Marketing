from dataclasses import asdict, dataclass
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

_ALLOWED_SCHEMES = {"http", "https"}
_UTM_KEYS = {"utm_source", "utm_medium", "utm_campaign"}


def _validate_text(value: str, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be a string")
    if any(ord(char) < 32 or ord(char) == 127 for char in value):
        raise ValueError(f"{field} must not contain control characters")
    value = value.strip()
    if not value:
        raise ValueError(f"{field} must not be empty")
    return value


@dataclass(frozen=True)
class Campaign:
    name: str
    channel: str
    objective: str
    source: str = "faceless-marketing"

    def __post_init__(self) -> None:
        for field in ("name", "channel", "objective", "source"):
            object.__setattr__(self, field, _validate_text(getattr(self, field), field))


def build_utm(base_url: str, campaign: Campaign) -> str:
    """Return a URL with deterministic UTM parameters.

    Existing UTM source/medium/campaign parameters are replaced rather than
    duplicated. URL fragments are preserved, and credentials in URLs are rejected.
    """
    if not isinstance(base_url, str) or not base_url.strip():
        raise ValueError("base_url must be a non-empty string")
    if any(ord(char) < 32 or ord(char) == 127 for char in base_url):
        raise ValueError("base_url must not contain control characters")

    parts = urlsplit(base_url.strip())
    if parts.scheme.lower() not in _ALLOWED_SCHEMES:
        raise ValueError("base_url must use http:// or https://")
    if not parts.hostname:
        raise ValueError("base_url must include a hostname")
    if parts.username is not None or parts.password is not None:
        raise ValueError("base_url must not contain embedded credentials")

    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in _UTM_KEYS
    ]
    query.extend(
        [
            ("utm_source", campaign.source),
            ("utm_medium", campaign.channel),
            ("utm_campaign", campaign.name),
        ]
    )
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def export_campaign(campaign: Campaign) -> dict:
    return asdict(campaign)
