from abc import ABC, abstractmethod

class LLMBaseClient(ABC):
    @abstractmethod
    def call(
            self,
            model: str,
            system_prompt: str,
            user_prompt: str,
            max_tokens: int,
            temperature: float,
            top_p: float,
    ) -> str:
        ...
