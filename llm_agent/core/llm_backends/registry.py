from typing import Dict, Type

from llm_agent.core.llm_backends.base_client import LLMBaseClient
from llm_agent.core.llm_backends.chatgpt_client import ChatGPTClient
from llm_agent.core.llm_backends.deepseek_client import DeepSeekClient
from llm_agent.core.llm_backends.gemini_client import GeminiClient


LLM_REGISTRY: Dict[str, Type[LLMBaseClient]] = {
    "gpt-4o": ChatGPTClient,
    "deepseek": DeepSeekClient,
    "gemini": GeminiClient,
}
