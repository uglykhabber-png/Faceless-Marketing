# Faceless Marketing

A local-first, open-source toolkit for ethical, measurable, non-personal-brand marketing of open-source software.

## What exists today

v0.2.0 provides:

- a typed campaign data model
- deterministic UTM URL generation
- safe URL validation
- replacement of existing UTM source/medium/campaign parameters
- a CLI for UTM generation and repository auditing
- JSON-ready campaign export helpers
- **Content brief schema** with Claim, KeywordCluster, and ContentBrief models
- **Keyword clustering** for content planning and SEO
- **ContentType enum** (release_note, technical_announcement, documentation_update, blog_post, tutorial, case_study)
- **ContentStatus enum** (draft, review, published, archived)
- Comprehensive validation against control characters, empty fields, and type mismatches
- Regression and adversarial tests (65 tests total)

The broader campaign-planning features described in the roadmap are **not implemented yet**. This distinction is deliberate: documentation should describe shipped behavior, not planned behavior.

## Quick start

```bash
python -m pip install -e .
faceless-marketing utm https://example.com/project --name launch --channel github --objective discoverability
```

Example output:

```text
https://example.com/project?utm_source=faceless-marketing&utm_medium=github&utm_campaign=launch
```

### Repository audit

```bash
faceless-marketing audit /path/to/repo --json
```

### Content brief (programmatic API)

```python
from faceless_marketing.content import (
    ContentType, ContentStatus,
    create_claim, create_keyword_cluster, create_content_brief
)
import json

claim = create_claim(
    text="Performance improved by 40%",
    evidence_source="benchmarks/q1_2024.json"
)

cluster = create_keyword_cluster(
    topic="performance",
    keywords=["fast", "benchmark", "optimization"],
    priority=8
)

brief = create_content_brief(
    id="release-v0.2",
    content_type=ContentType.RELEASE_NOTE,
    title="Version 0.2.0 Release",
    hypothesis="Users need to know about performance improvements",
    claims=[claim],
    target_audience="backend developers",
    channel="github",
    keyword_clusters=[cluster]
)

print(json.dumps(brief.as_dict(), indent=2))
```

## Scope

Faceless Marketing helps a project turn useful engineering work into discoverable, evidence-based marketing assets without fake engagement, fabricated metrics, spam, impersonation, or automated unsolicited outreach.

## Principles

1. No fake engagement.
2. No fabricated claims or metrics.
3. No impersonation.
4. No spam or unsolicited bulk outreach.
5. Preserve source attribution.
6. Prefer useful content over promotional noise.
7. Keep measurement reproducible.
8. Ship only what the documentation says is implemented.

## Development

```bash
python -m pip install -U pytest
python -m pytest -q
python -m compileall -q src
```

CI tests Python 3.10 through 3.13.

## Status

**v0.2.0 released.** Content brief schemas and keyword clustering now available. See `docs/CONTENT_BRIEF_SCHEMA.md` for detailed specification.
