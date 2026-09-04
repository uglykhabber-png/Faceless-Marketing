from __future__ import annotations

import json
from typing import Any


def to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def to_markdown(payload: dict[str, Any]) -> str:
    score = payload.get("score", "n/a")
    lines = [f"# Faceless Marketing Report", "", f"**Score:** {score}", ""]
    findings = payload.get("findings", [])
    if findings:
        lines += ["## Findings", ""]
        for finding in findings:
            lines += [f"- **{finding['rule_id']}** — {finding['title']} ({finding['severity']})", f"  - {finding['message']}", f"  - Fix: {finding['remediation']}"]
    gaps = payload.get("gaps", [])
    if gaps:
        lines += ["## Discoverability gaps", ""]
        for gap in gaps:
            lines += [f"- **{gap['gap_id']}** — {gap['title']}: {gap['rationale']}"]
    return "\n".join(lines) + "\n"
