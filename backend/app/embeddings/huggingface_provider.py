import os

from sentence_transformers import SentenceTransformer


class HuggingFaceEmbeddingProvider:
    def __init__(self) -> None:
        self.model_name = os.getenv(
            "EMBEDDING_MODEL",
            "BAAI/bge-small-en-v1.5",
        )

        self.model = SentenceTransformer(
            self.model_name,
        )

    def embed(self, text: str) -> list[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()