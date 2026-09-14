import ollama

from adapters.base import BaseLLMAdapter


class OllamaAdapter(BaseLLMAdapter):
    """
    Adapter for locally running Ollama models.
    """

    def __init__(
        self,
        model: str = "qwen2.5:3b",
    ):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]