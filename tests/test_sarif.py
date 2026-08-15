import json

from faceless_marketing.audit import AuditReport
from faceless_marketing.evidence import Evidence, Finding
from faceless_marketing.sarif import report_to_sarif
from faceless_marketing.cli import main


def sample_report():
    finding = Finding(
        rule_id="README_PRESENT",
        title="Missing README.md",
        severity="high",
        message="README.md is missing.",
        remediation="Add a README.",
        evidence=(Evidence("README_PRESENT", "README.md", "missing", "high"),),
    )
    return AuditReport(root=".", score=85, findings=(finding,))


def test_sarif_shape_is_stable():
    payload = report_to_sarif(sample_report())
    assert payload["version"] == "2.1.0"
    assert payload["runs"][0]["tool"]["driver"]["name"] == "faceless-marketing"
    assert payload["runs"][0]["results"][0]["ruleId"] == "README_PRESENT"
    json.dumps(payload, sort_keys=True)


def test_sarif_severity_mapping():
    payload = report_to_sarif(sample_report())
    assert payload["runs"][0]["results"][0]["level"] == "error"


def test_cli_rejects_conflicting_formats(tmp_path, capsys):
    (tmp_path / "README.md").write_text("# Example\n\n## Quick start\n\n```bash\nrun\n```\n" + "x" * 500)
    try:
        main(["audit", str(tmp_path), "--json", "--sarif"])
    except SystemExit as exc:
        assert exc.code == "choose only one of --json or --sarif"
    else:
        raise AssertionError("expected format conflict to fail")
