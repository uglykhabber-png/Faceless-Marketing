from pathlib import Path

import pytest

from faceless_marketing.audit import audit_repository


def test_findings_are_deterministic(tmp_path: Path):
    (tmp_path / "README.md").write_text("# Tiny", encoding="utf-8")
    first = audit_repository(tmp_path).as_dict()
    second = audit_repository(tmp_path).as_dict()
    assert first == second


def test_binary_readme_is_not_fatal(tmp_path: Path):
    (tmp_path / "README.md").write_bytes(b"\xff\xfe\x00\x00")
    report = audit_repository(tmp_path)
    assert 0 <= report.score <= 100


def test_non_directory_root_rejected(tmp_path: Path):
    target = tmp_path / "file.txt"
    target.write_text("x", encoding="utf-8")
    with pytest.raises(ValueError):
        audit_repository(target)
