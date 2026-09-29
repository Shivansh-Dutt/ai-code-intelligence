from functools import lru_cache

from app.llm.groq_provider import GroqProvider

@lru_cache(maxsize=1)
def get_llm_provider():
    return GroqProvider()