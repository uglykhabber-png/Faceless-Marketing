from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import re

from .evidence import Evidence, Finding


@dataclass(frozen=True)
class AuditReport:
    root: str
    score: int
    findings: tuple[Finding, ...]
    schema_version: int = 1

    def as_dict(self) -> dict:
        return {
            "schema_version": self.schema_version,
            "root": self.root,
            "score": self.score,
            "findings": [item.as_dict() for item in self.findings],
        }


def _finding(rule_id: str, title: str, severity: str, message: str, remediation: str, source: str) -> Finding:
    return Finding(
        rule_id=rule_id,
        title=title,
        severity=severity,
        message=message,
        remediation=remediation,
        evidence=(Evidence(rule_id, source, message, severity),),
    )


def audit_repository(root: str | Path) -> AuditReport:
    base = Path(root).resolve()
    if not base.is_dir():
        raise ValueError("root must be an existing directory")
    findings: list[Finding] = []
    points = 100
    checks = {
        "README_PRESENT": ("README.md", 15, "Add a README that explains the problem, installation and first useful run."),
        "LICENSE_PRESENT": ("LICENSE", 15, "Add an explicit open-source license."),
        "CONTRIBUTING_PRESENT": ("CONTRIBUTING.md", 10, "Add contribution instructions so external developers can contribute."),
        "SECURITY_PRESENT": ("SECURITY.md", 10, "Add a security policy with a private-reporting path."),
        "CHANGELOG_PRESENT": ("CHANGELOG.md", 10, "Add a changelog so releases have a traceable history."),
    }
    for rule_id, (filename, weight, remediation) in checks.items():
        if not (base / filename).is_file():
            points -= weight
            findings.append(_finding(rule_id, f"Missing {filename}", "high" if weight >= 15 else "medium", f"{filename} is not present at repository root.", remediation, str(base / filename)))

    security = base / "SECURITY.md"
    if security.exists():
        text = security.read_text(encoding="utf-8", errors="replace").lower()
        if not re.search(r"(private|security\s+advisory|report\s+privately|contact|security policy)", text):
            points -= 10
            findings.append(_finding("SECURITY_REPORTING_PATH", "Security reporting path is unclear", "high", "SECURITY.md does not expose a recognizable private-reporting mechanism.", "Document a private GitHub Security Advisory route, security contact, or other non-public reporting mechanism.", str(security)))

    readme = base / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < 400:
            points -= 10
            findings.append(_finding("README_DEPTH", "README is very short", "medium", "README.md contains fewer than 400 characters.", "Add a concise problem statement, quick start, example, limitations and contribution path.", str(readme)))
        if not any(marker in text for marker in ("```bash", "```sh", "```console", "Quick start", "Usage")):
            points -= 10
            findings.append(_finding("EXAMPLE_PRESENT", "No obvious usage example", "medium", "README has no recognized command/usage example marker.", "Add one copy-pasteable first-run example.", str(readme)))
        links = re.findall(r"https?://[^\s)\]>]+", text)
        bad = [link for link in links if urlparse(link).scheme not in {"http", "https"} or not urlparse(link).netloc]
        if bad:
            points -= 5
            findings.append(_finding("DOC_LINKS_VALID", "Malformed external links", "low", f"Found {len(bad)} malformed HTTP(S) link(s).", "Correct or remove malformed links before publishing documentation.", str(readme)))

    docs = base / "docs"
    if docs.exists() and docs.is_dir() and not list(docs.rglob("*.md")):
        points -= 5
        findings.append(_finding("DOCS_NONEMPTY", "Docs directory contains no Markdown files", "low", "A docs directory exists but contains no Markdown documentation.", "Add at least one focused usage or architecture document.", str(docs)))

    return AuditReport(root=str(base), score=max(0, points), findings=tuple(sorted(findings, key=lambda item: (item.rule_id, item.title))))
