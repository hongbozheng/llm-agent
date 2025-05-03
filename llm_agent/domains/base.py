from typing import Dict

from abc import ABC, abstractmethod
from llm_agent.core.prompt.schema import Prompt


class Domain(ABC):
    @abstractmethod
    def handle_prompt(self, prompt: Prompt) -> Dict:
        """Given parsed intent, return a recommended strategy."""
        ...
