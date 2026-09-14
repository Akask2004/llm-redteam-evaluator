from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response from the target LLM.

        Args:
            prompt: Input prompt.

        Returns:
            Model-generated response.
        """
        pass