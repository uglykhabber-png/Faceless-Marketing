# Faceless Marketing

A local-first, open-source toolkit for ethical, measurable, non-personal-brand marketing of open-source software.

## What exists today

v0.2 adds an evidence-first OSS growth intelligence foundation:

- deterministic UTM URL generation with safe URL validation
- repository audit with scored, evidence-linked findings
- campaign ledger primitives for deterministic campaign records
- explicit evidence records with provenance state, UTC timestamps and confidence
- discoverability-gap analysis grounded in repository content
- evidence-weighted decision scoring with an `INSUFFICIENT_EVIDENCE` outcome
- deterministic JSON/CSV/SARIF/Markdown reporting surfaces
- adversarial and contract tests

The project does **not** claim causal lift, ROI, conversions, traffic forecasts, fake engagement, or automated unsolicited outreach from metadata alone.

## Quick start

```bash
python -m pip install -e .
faceless-marketing utm https://example.com/project --name launch --channel github --objective discoverability
faceless-marketing audit .
faceless-marketing discover .
faceless-marketing report .
```

## Architecture

`RAW INPUT → VALIDATION → OBSERVATION → EVIDENCE → INTERPRETATION → RECOMMENDATION → ACTION`

See [`docs/LAYERS.md`](docs/LAYERS.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

## Security

Do not place secrets, credentials, private campaign data, or personal data in public issues or pull requests. Report vulnerabilities through the repository's private GitHub Security Advisory flow described in [`SECURITY.md`](SECURITY.md).

## Scope

Faceless Marketing helps projects turn useful engineering work into discoverable, evidence-based marketing assets without fake engagement, fabricated claims or metrics, spam, impersonation, or automated unsolicited outreach.

## Development

```bash
python -m pip install -U pytest
python -m pytest -q
python -m compileall -q src
```

CI tests Python 3.10 through 3.13 and validates the human and machine interfaces.

## Status

**v0.2 development line.** The repository is building toward an OSS Growth Intelligence Platform; shipped functionality remains deliberately narrower than future roadmap items.
