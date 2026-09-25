from pathlib import Path

from app.ingestion.files import discover_source_files


def test_discover_source_files(tmp_path: Path) -> None:
    (tmp_path / "main.py").write_text(
        "print('hello')"
    )

    (tmp_path / "README.md").write_text(
        "# Example"
    )

    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()

    (node_modules / "package.js").write_text(
        "console.log('ignored')"
    )

    files = discover_source_files(tmp_path)

    assert tmp_path / "main.py" in files
    assert tmp_path / "README.md" not in files
    assert node_modules / "package.js" not in files