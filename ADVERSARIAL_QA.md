# Adversarial QA

## Attack surface

- unsafe URL schemes
- missing URL hostnames
- embedded URL credentials
- control characters
- malformed campaign fields
- duplicate UTM parameters
- loss of existing query parameters
- loss of URL fragments
- non-deterministic output
- documentation claims that exceed shipped functionality
- fake-engagement or unsolicited-outreach workflows

## Findings and fixes

### A-001 — normalization bypass

**Input:** a campaign name containing a trailing newline.

**Observed:** the initial validator stripped whitespace before checking control characters, allowing the test case through.

**Fix:** control characters are now rejected before normalization.

**Status:** fixed and regression-tested.

### A-002 — duplicate UTM parameters

**Risk:** appending UTM parameters blindly can create multiple values for the same tracking key.

**Fix:** existing `utm_source`, `utm_medium`, and `utm_campaign` parameters are removed before deterministic replacement.

**Status:** fixed and regression-tested.

### A-003 — credential-bearing URLs

**Risk:** accepting embedded credentials could propagate secrets into generated links.

**Fix:** URLs containing username/password components are rejected.

**Status:** fixed and regression-tested.

## Release gate

The release is not considered validated until GitHub Actions passes the complete test matrix on Python 3.10–3.13.
