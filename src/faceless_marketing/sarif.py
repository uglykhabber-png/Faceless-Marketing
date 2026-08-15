from __future__ import annotations

from .audit import AuditReport

_SEVERITY = {"high": "error", "medium": "warning", "low": "note", "info": "note"}


def report_to_sarif(report: AuditReport) -> dict:
    rules = {}
    results = []
    for finding in report.findings:
        rules.setdefault(
            finding.rule_id,
            {
                "id": finding.rule_id,
                "name": finding.title,
                "shortDescription": {"text": finding.title},
                "help": {"text": finding.remediation},
            },
        )
        results.append(
            {
                "ruleId": finding.rule_id,
                "level": _SEVERITY.get(finding.severity, "warning"),
                "message": {"text": finding.message},
                "properties": {"severity": finding.severity},
            }
        )

    return {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "faceless-marketing",
                        "informationUri": "https://github.com/uglykhabber-png/Faceless-Marketing",
                        "rules": sorted(rules.values(), key=lambda item: item["id"]),
                    }
                },
                "automationDetails": {"id": "faceless-marketing/oss-audit"},
                "results": sorted(results, key=lambda item: (item["ruleId"], item["level"])),
            }
        ],
    }
