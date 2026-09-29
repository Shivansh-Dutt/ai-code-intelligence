from functools import lru_cache

from app.embeddings.huggingface_provider import (
    HuggingFaceEmbeddingProvider
)

@lru_cache(maxsize=1)
def get_embedding_provider():
    return HuggingFaceEmbeddingProvider()