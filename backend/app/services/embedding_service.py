from sqlalchemy.orm import Session

from app.embeddings.registry import get_embedding_provider
from app.models.repository_chunk import RepositoryChunk


EMBEDDING_BATCH_SIZE = 32


def embed_chunks(
    db: Session,
    chunks: list[RepositoryChunk],
) -> None:
    if not chunks:
        return

    provider = get_embedding_provider()

    for start in range(
        0,
        len(chunks),
        EMBEDDING_BATCH_SIZE,
    ):
        batch = chunks[
            start:start + EMBEDDING_BATCH_SIZE
        ]

        embeddings = provider.embed_many(
            [chunk.content for chunk in batch]
        )

        if len(embeddings) != len(batch):
            raise RuntimeError(
                "Embedding count does not match "
                "chunk count"
            )

        for chunk, embedding in zip(
            batch,
            embeddings,
            strict=True,
        ):
            chunk.embedding = embedding
            chunk.embedding_model = (
                provider.model_name
            )

        db.commit()