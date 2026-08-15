# Phase B — Campaign Ledger Certification

## Scope

Phase B provides a local-first, deterministic campaign ledger. It records campaign identity, asset identity, channel/source/destination, objective, hypothesis, publication time, result state, observed metrics and evidence provenance. UTM URLs are derived from the canonical campaign fields and are never treated as performance evidence.

## Data integrity rules

- Campaign and asset IDs are restricted to safe identifiers and are unique within a ledger.
- Publication timestamps must include an explicit timezone and are normalized to UTC.
- Destinations must be absolute HTTP(S) URLs and cannot contain embedded credentials.
- Metrics must be non-negative numeric observations.
- A measured campaign requires at least one metric.
- Recorded metrics require an evidence source.
- Metric names are unique within a campaign.
- Result states are limited to `planned`, `published`, `measured`, and `inconclusive`.
- JSON and CSV records are emitted in deterministic campaign-ID order.
- JSON has an explicit schema version (`1`).

## Attribution boundary

The ledger records observations. It does not infer conversions, causal lift, ROI, or growth from campaign metadata alone. A performance claim is valid only when the corresponding metric and evidence source are explicitly recorded.

## Privacy boundary

The core ledger does not require names, email addresses, access tokens, cookies, credentials, or user-level identifiers. Embedded URL credentials and control characters are rejected.

## Adversarial matrix

The Phase B test suite covers duplicate IDs, malformed URLs, embedded credentials, control characters, unsafe identifiers, ambiguous timestamps, negative metrics, boolean/non-numeric metrics, missing evidence, duplicate metric names, unsupported result states, invalid schema versions, malformed campaign entries, deterministic ordering and round-trip serialization.

## Certification gates

### R1 — Correctness

Schema validation, UTC normalization, deterministic JSON/CSV serialization, duplicate prevention, evidence requirements and round-trip behavior must pass.

### R2 — Adversarial robustness

Malformed or hostile input must fail closed without leaking credentials or accepting unsupported attribution states.

### R3 — Reproducibility

The package must remain compatible with the repository's supported Python versions, produce stable JSON/CSV output and pass CI in a clean environment.

### Merge rule

Phase B must not be declared certified until implementation, adversarial testing, R1, R2, R3 and CI evidence are all present. No invented conversion, performance, ROI or growth claim is permitted.
