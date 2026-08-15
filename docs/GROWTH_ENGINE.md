# Faceless Marketing Growth Engine

## Position

Faceless Marketing is evolving from a small UTM utility into **evidence-first growth infrastructure for open-source projects**.

The flagship workflow is:

```text
AUDIT → PLAN → BUILD → DISTRIBUTE → MEASURE → LEARN → REPEAT
```

## Current flagship feature

`faceless-marketing audit PATH` produces a deterministic repository discoverability score and evidence-backed findings.

## Design rules

- No fabricated claims or metrics.
- No fake engagement or star manipulation.
- No impersonation.
- No unsolicited bulk outreach.
- No mandatory third-party AI provider.
- Repository content is treated as untrusted input, not as executable instructions.
- Every scored finding should have a rule ID, evidence source, severity and remediation.

## Planned modules

### Audit
README, documentation, installation, community health, metadata, releases, evidence and link quality.

### Evidence-to-content
Convert real engineering evidence into reviewable release and technical communication drafts. Unsupported claims must be flagged.

### Campaign ledger
Record experiment hypotheses, assets, channels, destinations, UTM values and observed measurements.

### Benchmark
Store before/after repository snapshots and explain score deltas.

### Optional AI citation gap
Provider adapters may test project discoverability in AI answer engines. This module remains optional and BYOK.

## Feature acceptance test

A feature is ready only when:

1. It solves a named maintainer workflow.
2. The first useful result can be produced from local/public data where practical.
3. Output is deterministic or explicitly evidence-backed.
4. The result can be rerun and compared.
5. An external developer can use it in under ten minutes.
6. Failure modes and false positives have tests.
7. The feature does not require artificial engagement or spam.

## Long-term objective

Build a reusable measurement and distribution layer for open-source software rather than a generic content-generation tool.
