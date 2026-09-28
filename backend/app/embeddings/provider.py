from typing import Protocol

class EmbeddingProvider(Protocol):
    def embed(self,text:str) -> list[float]:
        ...
    
    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        ...