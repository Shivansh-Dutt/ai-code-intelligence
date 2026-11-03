import os
from pathlib import Path
from threading import Lock

DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"

# Keep the model inside the backend directory so a model downloaded
# at build time is reused at runtime.
DEFAULT_CACHE_DIR = str(
    Path(__file__).resolve().parents[2] / "models"
)


class LocalEmbeddingProvider:
    """Runs the embedding model in-process via fastembed (ONNX).

    Produces the same 384-dim, L2-normalised vectors as the hosted
    BAAI/bge-small-en-v1.5, so existing stored embeddings remain valid.
    """

    def __init__(self) -> None:
        self.model_name = os.getenv(
            "EMBEDDING_MODEL",
            DEFAULT_MODEL,
        )
        self._cache_dir = os.getenv(
            "EMBEDDING_CACHE_DIR",
            DEFAULT_CACHE_DIR,
        )
        self._model = None
        self._lock = Lock()

    def _get_model(self):
        # Lazy load: keeps app startup fast and memory low until needed.
        if self._model is None:
            with self._lock:
                if self._model is None:
                    from fastembed import TextEmbedding

                    self._model = TextEmbedding(
                        model_name=self.model_name,
                        cache_dir=self._cache_dir,
                    )
        return self._model

    def embed(self, text: str) -> list[float]:
        return self.embed_many([text])[0]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        model = self._get_model()

        normalized: list[list[float]] = []

        for array in model.embed(texts, batch_size=16):
            vector = [float(value) for value in array]
            norm = sum(value * value for value in vector) ** 0.5

            if norm == 0:
                raise RuntimeError(
                    "Embedding model returned a zero vector"
                )

            normalized.append(
                [value / norm for value in vector]
            )

        if len(normalized) != len(texts):
            raise RuntimeError(
                "Embedding count does not match input count"
            )

        return normalized
