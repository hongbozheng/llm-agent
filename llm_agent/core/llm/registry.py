from typing import Dict, Type

from .chatgpt_client import ChatGPTClient
from .deepseek_client import DeepSeekClient
from .gemini_client import GeminiClient

LLM_REGISTRY: Dict[str, Type] = {
    "gpt": ChatGPTClient,
    "deepseek": DeepSeekClient,
    "gemini": GeminiClient,
}
