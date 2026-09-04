from pathlib import Path

from faceless_marketing.audit import audit_repository
from faceless_marketing.evidence import EvidenceRecord


def test_security_reporting_path_is_audited(tmp_path: Path):
    for name, text in {
        "README.md": "# Example\n\n## Quick start\n\n```bash\nrun\n```\n" + "x" * 500,
        "LICENSE": "Apache-2.0",
        "CONTRIBUTING.md": "Contributing",
        "CHANGELOG.md": "Changelog",
        "SECURITY.md": "## Reporting vulnerabilities\nUse GitHub Security Advisory reporting flow privately.",
    }.items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    rules = {finding.rule_id for finding in audit_repository(tmp_path).findings}
    assert "SECURITY_REPORTING_PATH" not in rules


def test_evidence_record_normalizes_utc():
    item = EvidenceRecord("e1", "analytics.json", "Observed visits", observed_at="2026-08-15T10:00:00+05:00")
    assert item.as_dict()["observed_at"] == "2026-08-15T05:00:00Z"
