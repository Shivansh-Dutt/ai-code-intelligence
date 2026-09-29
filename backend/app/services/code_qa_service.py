from uuid import UUID

from sqlalchemy.orm import Session

from app.embeddings.registry import (
    get_embedding_provider,
)
from app.llm.registry import (
    get_llm_provider,
)
from app.services.retrieval import (
    build_context,
    deduplicate_results,
)
from app.services.search_service import search_repository

from dataclasses import dataclass

from app.services.retrieval import (
    RetrievalResult,
)

@dataclass(frozen=True)
class CodeAnswer:
    answer: str
    sources: list[RetrievalResult]

SYSTEM_PROMPT = """
You are an AI code intelligence assistant.

Answer questions about the repository using only
the supplied source-code context.

Citation requirements:
- Cite important factual claims about the code.
- Use the exact file path and line range supplied
  in the context.
- Format citations as [path:start-end].
- Never invent a citation.
- Never invent a file, function, class, or behavior.
- If the supplied context is insufficient, say so.

Be concise and technically precise.
"""


def answer_code_question(
    db: Session,
    repository_id: UUID,
    question: str,
    limit: int = 10,
) -> str:

    embedding_provider = get_embedding_provider()

    query_embedding = embedding_provider.embed(
        question
    )

    results = search_repository(
        db=db,
        repository_id=repository_id,
        query_embedding=query_embedding,
        limit=limit,
    )

    results = deduplicate_results(results)

    context = build_context(results)

    if not context:
        return (
            "I couldn't find sufficiently relevant "
            "code in this repository to answer that "
            "question."
        )

    user_prompt = f"""
Repository question:

{question}

Retrieved repository context:

{context}
"""

    llm = get_llm_provider()

    answer =  llm.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )
    
    return CodeAnswer(
        answer=answer,
        sources=results,
    )