from uuid import UUID

from sqlalchemy.orm import Session

from app.embeddings.huggingface_provider import (
    HuggingFaceEmbeddingProvider,
)
from app.llm.groq_provider import GroqProvider
from app.services.search_service import search_repository


SYSTEM_PROMPT = """
You are an AI code intelligence assistant.

Answer questions about the repository using only
the supplied source-code context.

Citation requirements:
- Cite every important factual claim about the code.
- Use the exact file path and line range supplied in context.
- Format citations as [path:start-end].
- Never invent a file path or line range.
- If the context does not contain enough information,
  explicitly say that the available context is insufficient.

Be precise and concise.
Distinguish directly observed code behavior from inference.
"""


def answer_code_question(
    db: Session,
    repository_id: UUID,
    question: str,
    limit: int = 8,
) -> str:
    embedding_provider = (
        HuggingFaceEmbeddingProvider()
    )

    query_embedding = embedding_provider.embed(
        question
    )

    results = search_repository(
        db=db,
        repository_id=repository_id,
        query_embedding=query_embedding,
        limit=limit,
    )

    context_parts = []

    for chunk, file, distance in results:
        context_parts.append(
            f"""
        SOURCE_ID: {chunk.id}
        FILE: {file.path}
        LINES: {chunk.start_line}-{chunk.end_line}
        
        {chunk.content}
        """
        )

    context = "\n---\n".join(context_parts)

    user_prompt = f"""
Repository question:

{question}

Repository context:

{context}
"""

    llm = GroqProvider()

    return llm.generate(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )