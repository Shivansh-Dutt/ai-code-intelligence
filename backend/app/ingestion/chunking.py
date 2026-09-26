from dataclasses import dataclass

@dataclass(frozen=True)
class SourceChunk:
    start_line: int
    end_line: int
    content: str

def chunk_source(
    content: str,
    max_lines: int=80,
    overlap_lines: int=10,
) -> list[SourceChunk]:
    lines = content.splitlines()
    
    if not lines:
        return []
    
    chunks: list[SourceChunk] = []
    
    start = 0
    
    while start < len(lines):
        end = min(
            start + max_lines,
            len(lines),
        )
        
        chunk_lines = lines[start:end]
        
        chunks.append(
            SourceChunk(
                start_line=start + 1,
                end_line=end,
                content="\n".join(chunk_lines)
            )
        )
        
        if end >= len(lines):
            break
        
        start = end - overlap_lines
        
    return chunks