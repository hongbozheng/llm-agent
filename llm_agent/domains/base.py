from abc import ABC, abstractmethod

from llm_agent.config import AgentConfig
from llm_agent.core.prompt.schema import Prompt


class Domain(ABC):
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg

    @abstractmethod
    def handle_prompt(self, prompt: Prompt) -> dict:
        """Given parsed intent, return a recommended strategy."""
        ...
