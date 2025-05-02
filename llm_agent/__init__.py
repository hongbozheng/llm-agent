"""
LLM Agent: A modular agent platform for generating and evaluating money-making strategies
across domains such as trading, crypto, real estate, and more.
"""

from .core.llm import LLMClient
from .core.schema import Prompt
from .core.prompt import PromptParser, PromptRouter

__all__ = [
    "LLMClient",
    "Prompt",
    "PromptParser",
    "PromptRouter",
]
