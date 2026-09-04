from pathlib import Path

import pytest

from faceless_marketing.decision import prioritize
from faceless_marketing.evidence import EvidenceRecord
from faceless_marketing.intelligence import analyze_discoverability


def test_discoverability_is_deterministic(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Project\n\n## Installation\n\nrun\n", encoding="utf-8")
    first = analyze_discoverability(tmp_path)
    second = analyze_discoverability(tmp_path)
    assert first == second
    assert [item.gap_id for item in first] == sorted(item.gap_id for item in first)


def test_missing_readme_is_explicit_gap(tmp_path: Path):
    gaps = analyze_discoverability(tmp_path)
    assert gaps[0].gap_id == "README_MISSING"


def test_decision_engine_can_refuse_low_evidence():
    result = prioritize(
        recommendation_id="r1",
        title="Investigate",
        action="Gather measurement evidence",
        expected_value=10,
        evidence=0.1,
        confidence=0.2,
    )
    assert result.status == "INSUFFICIENT_EVIDENCE"


def test_decision_engine_priority_is_reproducible():
    kwargs = dict(recommendation_id="r2", title="Docs", action="Improve docs", expected_value=10, evidence=0.8, reach=2, effort=1, risk=1, confidence=0.9)
    assert prioritize(**kwargs) == prioritize(**kwargs)


def test_evidence_record_rejects_naive_timestamp():
    with pytest.raises(ValueError):
        EvidenceRecord("e1", "source", "description", observed_at="2026-08-15T00:00:00")
