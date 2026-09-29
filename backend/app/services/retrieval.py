from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class RetrievalResult:
    chunk_id: UUID
    file_id: UUID
    path: str
    start_line: int
    end_line: int
    content: str
    distance: float
    
    @property
    def citation(self) -> str:
        return (
            f"[{self.path}:"
            f"{self.start_line}-{self.end_line}]"
        )
        
def deduplicate_results(
    results: list[RetrievalResult],
) -> list[RetrievalResult]:
    
    selected: list[RetrievalResult] = []
    
    for result in results:
        overlaps = False
        
        for existing in selected:
            if result.path != existing.path:
                continue
        
            if (
                result.start_line <= existing.end_line
                and result.end_line >= existing.start_line
            ):
                overlaps = True
                break
            
        if not overlaps:
            selected.append(result)
                
    return selected

def build_context(
    results: list[RetrievalResult],
    max_characters: int = 30_000,
) -> str:

    parts: list[str] = []
    total = 0

    for result in results:
        block = (
            f"FILE: {result.path}\n"
            f"LINES: {result.start_line}-"
            f"{result.end_line}\n"
            f"SOURCE_ID: {result.chunk_id}\n\n"
            f"{result.content}\n"
        )

        if total + len(block) > max_characters:
            break

        parts.append(block)
        total += len(block)

    return "\n---\n".join(parts)