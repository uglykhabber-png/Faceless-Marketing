# Threat model and adversarial gates

## Assets

- repository source and configuration
- campaign records and measurement provenance
- generated reports and machine-readable schemas
- contributor trust and attribution integrity

## Threat classes

### Input attacks

Malformed URLs, unsafe schemes, embedded credentials, control characters, pathological identifiers, duplicate IDs, hostile Unicode and malformed structured records must fail closed.

### Evidence attacks

Missing, stale, duplicated, contradictory or weakly sourced measurements must not be silently upgraded into facts.

### Reasoning attacks

The product must reject or clearly label correlation-as-causation, estimate-as-observation, absence-as-zero, and small-sample trends. Decision scoring must use explicit evidence and confidence inputs.

### Marketing abuse

The product must not automate fake engagement, fabricated testimonials or metrics, impersonation, spam, unsolicited bulk outreach, or deceptive attribution.

## Release gates

Every release should verify:

- unit and adversarial tests
- deterministic outputs
- package compilation
- schema stability
- documentation/implementation alignment
- security-reporting path
- CI on every supported Python version

A feature is not complete until code, tests, evidence, documentation, security policy and CI agree.
