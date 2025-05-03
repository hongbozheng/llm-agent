from typing import Dict, Type

from .base_client import LLMBaseClient
from .chatgpt_client import ChatGPTClient
from .deepseek_client import DeepSeekClient
from .gemini_client import GeminiClient


LLM_REGISTRY: Dict[str, Type[LLMBaseClient]] = {
    "gpt-4o": ChatGPTClient,
    "deepseek": DeepSeekClient,
    "gemini": GeminiClient,
}
