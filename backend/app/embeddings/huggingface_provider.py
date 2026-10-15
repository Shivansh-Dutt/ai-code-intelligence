
import os

from huggingface_hub import InferenceClient


class HuggingFaceEmbeddingProvider:
    def __init__(self) -> None:
        self.model_name = os.getenv(
            "EMBEDDING_MODEL",
            "BAAI/bge-small-en-v1.5",
        )

        token = os.getenv("HF_TOKEN")
        if not token:
            raise RuntimeError(
                "HF_TOKEN environment variable is required"
            )

        self.client = InferenceClient(
            model=self.model_name,
            token=token,
        )

    def embed(self, text: str) -> list[float]:
        return self.embed_many([text])[0]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        if not texts:
            return []

        result = self.client.feature_extraction(texts)
        vectors = result.tolist()

        # Some models return token-level vectors.
        # Mean-pool them to produce one vector per input.
        if vectors and vectors[0] and isinstance(
            vectors[0][0], list
        ):
            vectors = [
                [
                    sum(token[i] for token in sentence)
                    / len(sentence)
                    for i in range(len(sentence[0]))
                ]
                for sentence in vectors
            ]

        normalized = []

        for vector in vectors:
            norm = sum(value * value for value in vector) ** 0.5

            if norm == 0:
                raise RuntimeError(
                    "Hugging Face returned a zero embedding"
                )

            normalized.append(
                [value / norm for value in vector]
            )

        if len(normalized) != len(texts):
            raise RuntimeError(
                "Embedding count does not match input count"
            )

        return normalized
