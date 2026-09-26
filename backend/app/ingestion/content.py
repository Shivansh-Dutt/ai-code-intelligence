from pathlib import Path

MAX_FILE_SIZE_BYTES = 512*1024

def read_source_file(
    path: Path,
) -> str | None:
    if path.stat().st_size > MAX_FILE_SIZE_BYTES:
        return None
    
    try:
        return path.read_text(
            encoding="utf-8",
        )
    except UnicodeDecodeError:
        return None