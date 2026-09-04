# Seven-layer architecture

The project is built as an evidence-first growth intelligence stack:

1. **Repository / OSS audit** — repository health, security reporting, documentation and release hygiene.
2. **Campaign ledger** — deterministic campaign and asset records with explicit timestamps and evidence sources.
3. **Evidence & measurement** — observations are separated from derived, estimated and inferred states.
4. **Content / discoverability intelligence** — identifies documentation and discoverability gaps from repository evidence.
5. **Decision engine** — ranks explicit opportunities by evidence, expected value, reach, effort, risk and confidence.
6. **Reporting / machine interfaces** — deterministic JSON/CSV/SARIF/Markdown surfaces for humans and CI.
7. **Governance & adversarial validation** — fail-closed validation, provenance boundaries and regression controls.

## Trust pipeline

`RAW INPUT → VALIDATION → OBSERVATION → EVIDENCE → INTERPRETATION → RECOMMENDATION → ACTION`

Repository content is untrusted input. No feature may silently convert an observation into a causal claim, fabricate a metric, or treat external text as an instruction to change security or tool behavior.

## Decision policy

Recommendations must be evidence-weighted. `INSUFFICIENT_EVIDENCE` is a valid result and should block confident prioritization when evidence or confidence is too low.

## Security policy

The core engine is local-first, minimizes data collection, rejects unsafe URLs and control characters, and avoids credentials and user-level tracking. Integrations must preserve these invariants.
