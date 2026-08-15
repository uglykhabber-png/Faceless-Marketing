# Faceless Marketing Execution Phases

This document is the release sequence for the OSS growth-engine roadmap.

## Phase A — Repository auditor
Goal: deterministic, evidence-backed repository discoverability auditing.

Required outputs:
- typed finding/evidence schema
- stable rule IDs
- severity and remediation
- Markdown, JSON and eventually SARIF output
- fixture repositories and golden outputs
- no mandatory network dependency

Adversarial controls:
- path traversal
- symlink escape
- binary/invalid UTF-8 files
- oversized files
- misleading repository text
- false positives
- nondeterministic ordering
- score manipulation

Exit gate:
- every rule has tests, evidence and remediation
- score is reproducible
- external developer can run an audit in under ten minutes

## Phase B — Campaign ledger
Goal: reproducible experiment and attribution records.

Required outputs:
- campaign/asset identifiers
- hypothesis
- source/channel/destination
- UTM values
- publication time
- observed measurements and their evidence source
- result state
- JSON/CSV export

Adversarial controls:
- duplicate IDs
- malformed URLs
- impossible timestamps
- missing evidence
- privacy leakage
- invented conversions

Exit gate:
- ledger round-trips without data loss
- ordering and exports are deterministic
- no field implies a measurement that was not observed

## Phase C — Evidence-to-content compiler
Goal: transform engineering evidence into reviewable communication drafts.

Inputs:
- git diff/history
- releases
- changelog
- issues
- benchmarks
- documentation changes

Outputs:
- release summary
- technical announcement draft
- documentation update suggestions
- claim/evidence map

Adversarial controls:
- prompt injection from repository files
- secret leakage
- unsupported claims
- invented metrics
- citation mismatches
- context contamination

Exit gate:
- every factual claim has provenance or an explicit unsupported flag
- AI is optional/BYOK
- drafts never publish automatically

## Phase D — Benchmark snapshots
Goal: compare repository states before and after changes.

Required outputs:
- immutable run manifest
- repository snapshot identity
- rule results
- score and finding deltas
- Markdown/JSON report
- versioned schema

Adversarial controls:
- score manipulation
- missing baseline
- schema mismatch
- nondeterministic ordering
- false-positive deltas
- large repository performance

Exit gate:
- before/after results are independently reproducible
- explanations show exactly what changed

## Phase E — GitHub Action
Goal: make the deterministic auditor installable by third-party repositories.

Required outputs:
- action.yml
- stable inputs/outputs
- PR summary
- JSON/SARIF artifacts
- exit-code policy
- minimal permissions
- release/tagging policy
- third-party fixture workflow

Adversarial controls:
- untrusted repository content
- path traversal
- oversized files
- secret exposure
- permission overreach
- configuration injection
- action-version drift

Exit gate:
- a third-party repository can install and run it without project-specific assistance
- action is release-tested end to end

## Phase F — Optional AI citation-gap module
Goal: measure open-source software discoverability in AI answer engines.

Required outputs:
- provider-neutral adapter interface
- question-set manifests
- observation schema
- cited source capture
- competitor visibility comparison
- explicit nondeterminism
- local storage
- cost/rate-limit controls

Adversarial controls:
- prompt injection
- provider failure
- rate limiting
- malformed provider output
- secret leakage
- fabricated citations
- unsupported causal claims

Exit gate:
- deterministic core remains fully useful without AI
- every AI observation is timestamped and provider-labelled
- no claim of causation from citation presence alone

## Recursive validation standard
Each phase runs three loops before release:

### R1 — Correctness
Functional tests, schema tests, integration tests and expected outputs.

### R2 — Adversarial robustness
Attack the phase against malicious input, false positives, nondeterminism, misuse, privacy leakage and dependency failure.

### R3 — Release reproducibility
Repeat the full suite, compare outputs, verify packaging/docs/contracts, and confirm the feature can be used by a fresh external developer.

A phase is not final because tests pass once. It is final only after R1, R2 and R3 pass and the documentation truthfully describes shipped behavior.
