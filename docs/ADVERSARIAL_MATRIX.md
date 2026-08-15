# Adversarial Validation Matrix

The project uses three recursive release loops for every phase.

## R1 — Correctness

- valid input produces expected output
- schemas round-trip
- CLI exits correctly
- JSON is parseable
- ordering is stable
- missing required files produce documented findings

## R2 — Adversarial robustness

| Attack | Expected behavior |
|---|---|
| path traversal / escape | reject or remain inside requested root |
| symlink escape | never read outside allowed root |
| binary/invalid UTF-8 content | handle safely without crashing |
| enormous file | apply bounded processing policy |
| control characters | reject where schema permits only clean text |
| malicious repository instructions | treat as untrusted data |
| malformed URL | reject |
| embedded URL credentials | reject |
| duplicate UTM keys | replace deterministically |
| unknown severity | reject |
| invalid evidence object | reject |
| fabricated metric | require evidence or flag unsupported |
| missing benchmark baseline | fail closed; never invent comparison |
| provider outage | preserve deterministic core |
| rate limit | return explicit provider error; never fabricate result |
| secret/API key in content | never emit it as marketing output |

## R3 — Release reproducibility

- run the full suite on every supported Python version
- run package installation, not just source-import tests
- execute installed CLI commands
- compare deterministic JSON output against fixtures
- verify docs match shipped behavior
- verify no credentials are present
- verify release artifacts contain expected files only

## Phase-specific attacks

### Phase A
False positives, score manipulation, path traversal, symlinks, malformed/binary files, nondeterministic traversal.

### Phase B
Duplicate campaign IDs, ambiguous timestamps, malformed destinations, unsupported conversions, private-data leakage, inconsistent exports.

### Phase C
Prompt injection in repository files, unsupported claims, fabricated metrics, secret leakage, provenance mismatch, accidental autonomous posting.

### Phase D
Missing baselines, schema version collisions, score tampering, nondeterministic snapshots, misleading deltas, large-repository performance.

### Phase E
Action permission overreach, untrusted repository execution, unsafe paths, oversized inputs, output injection, action-version drift.

### Phase F
Provider errors, rate limits, malformed answers, fabricated citations, source misattribution, prompt injection, unsupported causal conclusions.

## Final principle

A phase is not considered complete because its happy-path tests pass. It is complete only when the adversarial matrix has been exercised, failures are corrected or explicitly documented, and R3 shows reproducible release behavior.
