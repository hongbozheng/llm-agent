from typing import Dict

from ..core.schema import Prompt
from abc import ABC, abstractmethod


class Domain(ABC):
    @abstractmethod
    def handle_prompt(self, prompt: Prompt) -> Dict:
        """Given parsed intent, return a recommended strategy."""
        ...
