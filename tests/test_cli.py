from faceless_marketing.cli import main


def test_audit_cli_json(tmp_path, capsys):
    (tmp_path / "README.md").write_text(
        "# Project\n\n## Quick start\n\n```bash\nrun\n```\n" + "x" * 500,
        encoding="utf-8",
    )
    (tmp_path / "LICENSE").write_text("Apache-2.0", encoding="utf-8")
    (tmp_path / "SECURITY.md").write_text("security", encoding="utf-8")
    (tmp_path / "CONTRIBUTING.md").write_text("contributing", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text("changelog", encoding="utf-8")
    assert main(["audit", str(tmp_path), "--json"]) == 0
    output = capsys.readouterr().out
    assert '"score"' in output
    assert '"findings"' in output
