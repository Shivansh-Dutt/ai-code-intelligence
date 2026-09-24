from urllib.parse import urlparse


def validate_github_repository_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)

    if parsed.scheme != "https":
        raise ValueError("GitHub URL must use HTTPS")

    if parsed.netloc.lower() != "github.com":
        raise ValueError("URL must point to github.com")

    parts = [
        part
        for part in parsed.path.split("/")
        if part
    ]

    if len(parts) != 2:
        raise ValueError(
            "URL must have the form https://github.com/{owner}/{repository}"
        )

    owner, repository = parts

    if repository.endswith(".git"):
        repository = repository[:-4]

    if not owner or not repository:
        raise ValueError("GitHub owner and repository are required")

    return owner, repository