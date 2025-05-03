from ..logger import log
from .registry import LLM_REGISTRY


class LLMClient:
    """Unified entrypoint for calling different LLM providers."""

    @staticmethod
    def call(
            llm: str,
            system_prompt: str,
            user_prompt: str,
            max_tokens: int = 1024,
            temperature: float = 0.5,
            top_p: float = 0.8,
    ) -> str:
        if llm not in LLM_REGISTRY:
            log(f"❌ [ERROR] Unsupported LLM `{llm}`")
            log(f"[ERROR] Choose from {{{LLM_REGISTRY.keys()}}}")
        try:
            client = LLM_REGISTRY[llm]
            return client.call(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
            )

            log(f"❌ [ERROR] Unsupported LLM backend: {llm}")
            raise

        except Exception as e:
            log(f"❌ [ERROR] Failed `{llm}` call")
            log(f"❌ [ERROR] Exception: {e}")
            raise
