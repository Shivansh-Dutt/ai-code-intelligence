from app.ingestion.chunking import chunk_source

def test_empty_source() -> None:
    assert chunk_source("") == []

def test_small_source() -> None:
    content = "\n".join(
        f"line {number}"
        for number in range(1, 6)
    )
    
    chunks = chunk_source(
        content,
        max_lines=10,
        overlap_lines=2,
    )
    
    assert len(chunks) == 1
    assert chunks[0].start_line == 1
    assert chunks[0].end_line == 5
    
def test_large_source() -> None:
    content = "\n".join(
        f"line {number}"
        for number in range(1, 101)
    )

    chunks = chunk_source(
        content,
        max_lines=20,
        overlap_lines=5,
    )

    assert len(chunks) == 7

    assert chunks[0].start_line == 1
    assert chunks[0].end_line == 20

    assert chunks[1].start_line == 16
    assert chunks[1].end_line == 35