# Faceless Marketing

A local-first, open-source toolkit for ethical, measurable, non-personal-brand marketing of open-source software.

## What exists today

v0.1.0 is intentionally small. It currently provides:

- a typed campaign data model
- deterministic UTM URL generation
- safe URL validation
- replacement of existing UTM source/medium/campaign parameters
- a CLI for UTM generation
- JSON-ready campaign export helpers
- regression and adversarial tests

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

**v0.1.0 release candidate.** The project is early-stage and should not be presented as a full marketing automation platform yet.
