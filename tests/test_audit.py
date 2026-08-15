from pathlib import Path

from faceless_marketing.audit import audit_repository


def write_repo(root: Path, *, readme: bool = True, license_file: bool = True) -> None:
    if readme:
        (root / "README.md").write_text(
            "# Example\n\nA useful example repository.\n\n## Quick start\n\n```bash\nexample run\n```\n" + "x" * 500,
            encoding="utf-8",
        )
    if license_file:
        (root / "LICENSE").write_text("Apache-2.0", encoding="utf-8")
    (root / "SECURITY.md").write_text("security", encoding="utf-8")
    (root / "CONTRIBUTING.md").write_text("contributing", encoding="utf-8")
    (root / "CHANGELOG.md").write_text("# Changelog", encoding="utf-8")


def test_good_repository_has_high_score(tmp_path):
    write_repo(tmp_path)
    report = audit_repository(tmp_path)
    assert report.score >= 90
    assert not [f for f in report.findings if f.rule_id in {"README_PRESENT", "LICENSE_PRESENT"}]


def test_missing_readme_and_license_is_penalized(tmp_path):
    write_repo(tmp_path, readme=False, license_file=False)
    report = audit_repository(tmp_path)
    rules = {f.rule_id for f in report.findings}
    assert "README_PRESENT" in rules
    assert "LICENSE_PRESENT" in rules
    assert report.score <= 75


def test_invalid_root_rejected(tmp_path):
    missing = tmp_path / "missing"
    try:
        audit_repository(missing)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
