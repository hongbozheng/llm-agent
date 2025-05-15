from llm_agent.config import AgentConfig
from llm_agent.core.prompt.schema import Prompt
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.io.writer import Writer
from typing import Optional

from abc import ABC, abstractmethod


class Domain(ABC):
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg

    @abstractmethod
    def process_prompt(
            self,
            prompt: Prompt,
            logger: Optional[ConversationLogger] = None,
            writer: Optional[Writer] = None,
    ) -> dict:
        """Given parsed intent, return a recommended strategy."""
        ...
