from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re
from typing import Any


@dataclass(frozen=True)
class ContentGap:
    gap_id: str
    title: str
    rationale: str
    evidence_source: str
    confidence: float = 1.0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def analyze_discoverability(root: str | Path) -> tuple[ContentGap, ...]:
    base = Path(root).resolve()
    if not base.is_dir():
        raise ValueError("root must be an existing directory")
    candidates: list[ContentGap] = []
    readme = base / "README.md"
    if not readme.exists():
        candidates.append(ContentGap("README_MISSING", "Add a repository entry point", "README.md is absent, creating a direct discoverability and onboarding gap.", "README.md"))
        return tuple(candidates)
    text = readme.read_text(encoding="utf-8", errors="replace")
    normalized = text.lower()
    required_sections = {
        "installation": ("installation", "Add installation instructions that a new contributor can execute."),
        "usage": ("usage", "Add a concise usage section with a copy-pasteable example."),
        "limitations": ("limitations", "Document current boundaries so users can distinguish shipped behavior from roadmap items."),
        "security": ("security", "Expose the security/reporting path from the primary documentation."),
        "contributing": ("contributing", "Give external contributors a clear contribution path."),
    }
    for key, (section, rationale) in required_sections.items():
        if not re.search(rf"^#+\s+.*{re.escape(section)}", normalized, re.MULTILINE):
            candidates.append(ContentGap(
                f"README_{key.upper()}_GAP",
                f"Strengthen README {section} coverage",
                rationale,
                "README.md",
            ))
    docs = base / "docs"
    if docs.exists() and not any(docs.rglob("*.md")):
        candidates.append(ContentGap("DOCS_EMPTY", "Add focused documentation", "The docs directory contains no Markdown guides.", "docs/"))
    return tuple(sorted(candidates, key=lambda item: item.gap_id))


@dataclass(frozen=True)
class IntelligenceReport:
    root: str
    gaps: tuple[ContentGap, ...]

    @property
    def score(self) -> int:
        penalty = min(100, len(self.gaps) * 10)
        return max(0, 100 - penalty)

    def as_dict(self) -> dict[str, Any]:
        return {"schema_version": 1, "root": self.root, "score": self.score, "gaps": [gap.as_dict() for gap in self.gaps]}


def intelligence_report(root: str | Path) -> IntelligenceReport:
    base = Path(root).resolve()
    return IntelligenceReport(str(base), analyze_discoverability(base))
