from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):

    @abstractmethod
    def generate(self, prompt: str, probe_id: str | None = None) -> str:
        pass