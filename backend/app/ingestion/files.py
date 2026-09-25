from pathlib import Path

IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
}

SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cs",
    ".rb",
    ".php",
    ".swift",
    ".kt",
    ".kts",
}

def discover_source_files(
    repository_path: Path,
) -> list[Path]:
    files: list[Path] = []
    
    for path in repository_path.rglob("*"):
        if not path.is_file():
            continue
        
        if any(
            part in IGNORED_DIRECTORIES
            for part in path.parts
        ):
            continue
        
        if path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        
        files.append(path)
        
    return sorted(files)
