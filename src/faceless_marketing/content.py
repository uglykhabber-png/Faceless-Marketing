from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any
from enum import Enum


class ContentStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ContentType(Enum):
    RELEASE_NOTE = "release_note"
    TECHNICAL_ANNOUNCEMENT = "technical_announcement"
    DOCUMENTATION_UPDATE = "documentation_update"
    BLOG_POST = "blog_post"
    TUTORIAL = "tutorial"
    CASE_STUDY = "case_study"


@dataclass(frozen=True)
class Claim:
    """A factual claim with mandatory evidence provenance."""
    text: str
    evidence_source: str
    rule_id: str | None = None
    unsupported: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("claim text must be a non-empty string")
        if not isinstance(self.evidence_source, str) or not self.evidence_source.strip():
            raise ValueError("evidence_source must be a non-empty string")
        if any(ord(c) < 32 or ord(c) == 127 for c in self.text):
            raise ValueError("claim text must not contain control characters")
        if any(ord(c) < 32 or ord(c) == 127 for c in self.evidence_source):
            raise ValueError("evidence_source must not contain control characters")

    def as_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "evidence_source": self.evidence_source,
            "rule_id": self.rule_id,
            "unsupported": self.unsupported,
        }


@dataclass(frozen=True)
class KeywordCluster:
    """A group of related keywords for content planning."""
    topic: str
    keywords: tuple[str, ...]
    priority: int = 5

    def __post_init__(self) -> None:
        if not isinstance(self.topic, str) or not self.topic.strip():
            raise ValueError("topic must be a non-empty string")
        if not isinstance(self.keywords, tuple) or len(self.keywords) == 0:
            raise ValueError("keywords must be a non-empty tuple")
        for kw in self.keywords:
            if not isinstance(kw, str) or not kw.strip():
                raise ValueError("each keyword must be a non-empty string")
            if any(ord(c) < 32 or ord(c) == 127 for c in kw):
                raise ValueError("keywords must not contain control characters")
        if not isinstance(self.priority, int) or not (1 <= self.priority <= 10):
            raise ValueError("priority must be an integer between 1 and 10")
        object.__setattr__(self, "topic", self.topic.strip())
        object.__setattr__(self, "keywords", tuple(k.strip() for k in self.keywords))

    def as_dict(self) -> dict[str, Any]:
        return {
            "topic": self.topic,
            "keywords": list(self.keywords),
            "priority": self.priority,
        }


@dataclass(frozen=True)
class ContentBrief:
    """Structured brief for transforming engineering evidence into content."""
    id: str
    content_type: ContentType
    title: str
    hypothesis: str
    claims: tuple[Claim, ...]
    target_audience: str
    channel: str
    status: ContentStatus = ContentStatus.DRAFT
    keyword_clusters: tuple[KeywordCluster, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("id must be a non-empty string")
        if not isinstance(self.content_type, ContentType):
            raise ValueError("content_type must be a ContentType enum")
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(self.hypothesis, str) or not self.hypothesis.strip():
            raise ValueError("hypothesis must be a non-empty string")
        if not isinstance(self.claims, tuple):
            raise ValueError("claims must be a tuple")
        if len(self.claims) == 0:
            raise ValueError("at least one claim is required")
        if not all(isinstance(c, Claim) for c in self.claims):
            raise ValueError("all claims must be Claim instances")
        if not isinstance(self.target_audience, str) or not self.target_audience.strip():
            raise ValueError("target_audience must be a non-empty string")
        if not isinstance(self.channel, str) or not self.channel.strip():
            raise ValueError("channel must be a non-empty string")
        if not isinstance(self.status, ContentStatus):
            raise ValueError("status must be a ContentStatus enum")
        if not isinstance(self.keyword_clusters, tuple):
            raise ValueError("keyword_clusters must be a tuple")
        if not all(isinstance(kc, KeywordCluster) for kc in self.keyword_clusters):
            raise ValueError("all keyword_clusters must be KeywordCluster instances")
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dict")

        for field_name in ("id", "title", "hypothesis", "target_audience", "channel"):
            value = getattr(self, field_name)
            if any(ord(c) < 32 or ord(c) == 127 for c in value):
                raise ValueError(f"{field_name} must not contain control characters")
            object.__setattr__(self, field_name, value.strip())

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "content_type": self.content_type.value,
            "title": self.title,
            "hypothesis": self.hypothesis,
            "claims": [c.as_dict() for c in self.claims],
            "target_audience": self.target_audience,
            "channel": self.channel,
            "status": self.status.value,
            "keyword_clusters": [kc.as_dict() for kc in self.keyword_clusters],
            "metadata": self.metadata,
        }


def create_claim(text: str, evidence_source: str, rule_id: str | None = None, unsupported: bool = False) -> Claim:
    """Factory function to create a validated Claim."""
    return Claim(text=text, evidence_source=evidence_source, rule_id=rule_id, unsupported=unsupported)


def create_keyword_cluster(topic: str, keywords: list[str], priority: int = 5) -> KeywordCluster:
    """Factory function to create a validated KeywordCluster."""
    return KeywordCluster(topic=topic, keywords=tuple(keywords), priority=priority)


def create_content_brief(
    id: str,
    content_type: ContentType,
    title: str,
    hypothesis: str,
    claims: list[Claim],
    target_audience: str,
    channel: str,
    status: ContentStatus = ContentStatus.DRAFT,
    keyword_clusters: list[KeywordCluster] | None = None,
    metadata: dict[str, str] | None = None,
) -> ContentBrief:
    """Factory function to create a validated ContentBrief."""
    return ContentBrief(
        id=id,
        content_type=content_type,
        title=title,
        hypothesis=hypothesis,
        claims=tuple(claims),
        target_audience=target_audience,
        channel=channel,
        status=status,
        keyword_clusters=tuple(keyword_clusters) if keyword_clusters else (),
        metadata=metadata if metadata else {},
    )
