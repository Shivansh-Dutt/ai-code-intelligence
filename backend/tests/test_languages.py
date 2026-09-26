from pathlib import Path

from app.ingestion.languages import detect_language


def test_detect_python() -> None:
    assert detect_language(
        Path("example.py")
    ) == "python"
    
def test_detect_typescript() -> None:
    assert detect_language(
        Path("example.ts")
    ) == "typescript"
    
def test_unknown_language() -> None:
    assert detect_language(
        Path("example.xyz")
    ) is None