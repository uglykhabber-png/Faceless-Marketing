# Architecture

## Product position

Faceless Marketing is evidence-first growth infrastructure for open-source projects. The core product loop is:

`AUDIT → PLAN → BUILD → DISTRIBUTE → MEASURE → LEARN → REPEAT`

## Layers

1. **Deterministic core** — typed data models, validators, scoring, campaign ledger and report generation.
2. **Audit engine** — repository-local/public-data checks that return stable rule IDs, evidence, severity and remediation.
3. **Content/evidence layer** — converts verified engineering evidence into reviewable communication artifacts. It must never invent unsupported claims.
4. **Measurement layer** — campaigns, UTM metadata, observed results and benchmark snapshots with explicit provenance.
5. **Integration layer** — GitHub Action and optional provider adapters. Integrations must not weaken the deterministic core.
6. **Optional AI layer** — BYOK/provider-neutral citation-gap analysis only after the core is independently useful.

## Trust boundary

Repository files, issue bodies, release notes and external text are **untrusted input**. They are data to inspect, not instructions to execute. The engine must not treat repository content as an authority over tool behavior, credentials, network access or system policy.

## Scoring contract

Scores are derived from explicit rules. Every finding contains:

- `rule_id`
- title
- severity
- message
- remediation
- evidence source(s)

Scores must be reproducible for the same repository snapshot and configuration. A numeric score without explanations is not a valid product output.

## Data contracts

The public JSON schemas will be versioned before Phase B. Backward-compatible additions are preferred; breaking changes require a schema version and migration note.

## Phase dependencies

Phase A is the foundation.
Phase B depends on stable campaign/evidence identifiers from A.
Phase C depends on evidence models from A and change/asset identifiers from B.
Phase D depends on stable audit output and benchmark manifests from A–C.
Phase E wraps the deterministic A/D engine for third-party repositories.
Phase F is optional and must remain detachable from A–E.

## Explicit non-goals

- fake stars or engagement
- automated unsolicited outreach
- impersonation
- credential harvesting
- mandatory third-party AI
- unexplained vanity metrics
- claims of causal marketing impact without observed evidence
