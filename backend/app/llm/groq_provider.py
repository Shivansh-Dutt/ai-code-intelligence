import os

from groq import Groq

from dotenv import load_dotenv

load_dotenv()

class GroqProvider:
    def __init__(self) -> None:
        self.client = Groq(
            api_key=os.environ["GROQ_API_KEY"]
        )

        self.model = os.getenv(
            "GROQ_MODEL",
            "qwen/qwen3.8-27b",
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0.1,
        )

        return response.choices[0].message.content or ""