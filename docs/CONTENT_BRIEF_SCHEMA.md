# Content Brief Schema Specification

## Overview

The content brief schema transforms engineering evidence into reviewable communication drafts. Every factual claim must have provenance or be explicitly flagged as unsupported.

## Core Models

### Claim

A factual claim with mandatory evidence provenance.

```python
@dataclass(frozen=True)
class Claim:
    text: str                    # The factual claim
    evidence_source: str         # Source of evidence (file, benchmark, etc.)
    rule_id: str | None          # Optional rule reference
    unsupported: bool            # Flag for unverified claims
```

**Validation rules:**
- `text` must be non-empty string without control characters
- `evidence_source` must be non-empty string without control characters
- `unsupported` defaults to `False`; must be explicitly set for unverified claims

### KeywordCluster

A group of related keywords for content planning and SEO.

```python
@dataclass(frozen=True)
class KeywordCluster:
    topic: str                   # Cluster topic name
    keywords: tuple[str, ...]    # Related keywords
    priority: int                # Priority 1-10 (default: 5)
```

**Validation rules:**
- `topic` must be non-empty string
- `keywords` must be non-empty tuple of non-empty strings
- `priority` must be integer between 1 and 10
- All strings are stripped of leading/trailing whitespace

### ContentBrief

Structured brief for transforming engineering evidence into content.

```python
@dataclass(frozen=True)
class ContentBrief:
    id: str                      # Unique identifier
    content_type: ContentType    # Type of content
    title: str                   # Working title
    hypothesis: str              # What this content tests
    claims: tuple[Claim, ...]    # Factual claims with evidence
    target_audience: str         # Intended audience
    channel: str                 # Distribution channel
    status: ContentStatus        # Workflow status
    keyword_clusters: tuple[KeywordCluster, ...]  # SEO clusters
    metadata: dict[str, str]     # Additional metadata
```

**Validation rules:**
- All text fields must be non-empty without control characters
- At least one `Claim` is required
- All claims must be validated `Claim` instances
- All keyword clusters must be validated `KeywordCluster` instances

## Enums

### ContentType

```python
class ContentType(Enum):
    RELEASE_NOTE = "release_note"
    TECHNICAL_ANNOUNCEMENT = "technical_announcement"
    DOCUMENTATION_UPDATE = "documentation_update"
    BLOG_POST = "blog_post"
    TUTORIAL = "tutorial"
    CASE_STUDY = "case_study"
```

### ContentStatus

```python
class ContentStatus(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"
    ARCHIVED = "archived"
```

## Factory Functions

```python
def create_claim(text: str, evidence_source: str, 
                 rule_id: str | None = None, 
                 unsupported: bool = False) -> Claim

def create_keyword_cluster(topic: str, keywords: list[str], 
                           priority: int = 5) -> KeywordCluster

def create_content_brief(id: str, content_type: ContentType, 
                         title: str, hypothesis: str, 
                         claims: list[Claim], 
                         target_audience: str, channel: str,
                         status: ContentStatus = ContentStatus.DRAFT,
                         keyword_clusters: list[KeywordCluster] | None = None,
                         metadata: dict[str, str] | None = None) -> ContentBrief
```

## JSON Serialization

All models implement `as_dict()` for deterministic JSON serialization:

```python
brief = create_content_brief(...)
json_ready = brief.as_dict()
# {
#   "id": "brief-001",
#   "content_type": "release_note",
#   "title": "...",
#   "claims": [{"text": "...", "evidence_source": "...", ...}],
#   ...
# }
```

## Adversarial Controls

| Attack | Defense |
|--------|---------|
| Prompt injection from repo files | Claims require explicit evidence_source |
| Unsupported claims | `unsupported` flag must be set explicitly |
| Fabricated metrics | No numeric claims without evidence source |
| Secret leakage | Control character validation on all fields |
| Empty/null injection | All required fields validated for non-empty values |
| Type confusion | Strict type checking on all constructor arguments |

## Design Principles

1. **Evidence-first**: Every claim traces to a source
2. **Explicit unsupported**: Unverified claims are flagged, not hidden
3. **Deterministic**: Same input produces identical JSON output
4. **Local-first**: No network calls required for validation
5. **Type-safe**: Frozen dataclasses prevent mutation
6. **Human-reviewable**: All drafts require manual approval before publication

## Usage Example

```python
from faceless_marketing.content import (
    ContentType, ContentStatus,
    create_claim, create_keyword_cluster, create_content_brief
)

# Create evidence-backed claims
claim1 = create_claim(
    text="Performance improved by 40%",
    evidence_source="benchmarks/q1_2024.json",
    rule_id="BENCHMARK_001"
)

claim2 = create_claim(
    text="New API endpoint added",
    evidence_source="CHANGELOG.md",
    unsupported=False
)

# Create keyword clusters
seo_cluster = create_keyword_cluster(
    topic="performance",
    keywords=["fast", "benchmark", "optimization"],
    priority=8
)

# Assemble content brief
brief = create_content_brief(
    id="release-v0.2",
    content_type=ContentType.RELEASE_NOTE,
    title="Version 0.2.0 Release",
    hypothesis="Users need to know about performance improvements",
    claims=[claim1, claim2],
    target_audience="backend developers",
    channel="github",
    status=ContentStatus.DRAFT,
    keyword_clusters=[seo_cluster],
    metadata={"version": "0.2.0"}
)

# Export for review
import json
print(json.dumps(brief.as_dict(), indent=2))
```

## Phase Alignment

This schema implements Phase B/C requirements from PHASES.md:
- Campaign/asset identifiers (`id` field)
- Hypothesis tracking
- Evidence-backed claims
- JSON export capability
- Explicit unsupported claim flagging
- Deterministic output
