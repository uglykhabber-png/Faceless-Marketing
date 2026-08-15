from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from .evidence import Evidence, Finding


@dataclass(frozen=True)
class AuditReport:
    root: str
    score: int
    findings: tuple[Finding, ...]

    def as_dict(self) -> dict:
        return {
            "root": self.root,
            "score": self.score,
            "findings": [item.as_dict() for item in self.findings],
        }


RULES = (
    "README_PRESENT",
    "LICENSE_PRESENT",
    "CONTRIBUTING_PRESENT",
    "SECURITY_PRESENT",
    "EXAMPLE_PRESENT",
    "CHANGELOG_PRESENT",
    "DOC_LINKS_VALID",
)


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
    checks = {
        "README_PRESENT": ("README.md", "Add a README that explains the problem, installation and first useful run."),
        "LICENSE_PRESENT": ("LICENSE", "Add an explicit open-source license."),
        "CONTRIBUTING_PRESENT": ("CONTRIBUTING.md", "Add contribution instructions so external developers can contribute."),
        "SECURITY_PRESENT": ("SECURITY.md", "Add a security policy with a private-reporting path."),
        "CHANGELOG_PRESENT": ("CHANGELOG.md", "Add a changelog so releases have a traceable history."),
    }

    points = 100
    for rule_id, (filename, remediation) in checks.items():
        if not (base / filename).exists():
            weight = 15 if rule_id in {"README_PRESENT", "LICENSE_PRESENT"} else 10
            points -= weight
            findings.append(
                _finding(
                    rule_id,
                    f"Missing {filename}",
                    "high" if weight >= 15 else "medium",
                    f"{filename} is not present at repository root.",
                    remediation,
                    str(base / filename),
                )
            )

    readme = base / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8", errors="replace")
        if len(text.strip()) < 400:
            points -= 10
            findings.append(
                _finding(
                    "README_DEPTH",
                    "README is very short",
                    "medium",
                    "README.md contains fewer than 400 characters.",
                    "Add a concise problem statement, quick start, example, limitations and contribution path.",
                    str(readme),
                )
            )
        example_markers = ("```bash", "```sh", "```console", "Quick start", "Usage")
        if not any(marker in text for marker in example_markers):
            points -= 10
            findings.append(
                _finding(
                    "EXAMPLE_PRESENT",
                    "No obvious usage example",
                    "medium",
                    "README has no recognized command/usage example marker.",
                    "Add one copy-pasteable first-run example.",
                    str(readme),
                )
            )

    docs = base / "docs"
    if docs.exists() and docs.is_dir():
        markdown_files = list(docs.rglob("*.md"))
        if not markdown_files:
            points -= 5
            findings.append(
                _finding(
                    "DOCS_NONEMPTY",
                    "Docs directory contains no Markdown files",
                    "low",
                    "A docs directory exists but contains no Markdown documentation.",
                    "Add at least one focused usage or architecture document.",
                    str(docs),
                )
            )

    links = []
    if readme.exists():
        import re
        links = re.findall(r"https?://[^\s)\]>]+", readme.read_text(encoding="utf-8", errors="replace"))
    bad = []
    for link in links:
        parsed = urlparse(link)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            bad.append(link)
    if bad:
        points -= 5
        findings.append(
            _finding(
                "DOC_LINKS_VALID",
                "Malformed external links",
                "low",
                f"Found {len(bad)} malformed HTTP(S) link(s).",
                "Correct or remove malformed links before publishing documentation.",
                str(readme),
            )
        )

    return AuditReport(root=str(base), score=max(0, points), findings=tuple(findings))
