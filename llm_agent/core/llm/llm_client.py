from ..logger import log
from .registry import LLM_REGISTRY


class LLMClient:
    """Unified entrypoint for calling different LLM providers."""

    @staticmethod
    def call(
        llm: str,
        system_prompt: str,
        user_prompt: str,
        top_p: float = 0.8,
    ) -> str:
        try:
            for keyword, client_class in LLM_REGISTRY.items():
                if llm.startswith(keyword):
                    client = client_class()
                    return client.call(
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        top_p=top_p,
                    )

            log(f"❌ [ERROR] Unsupported LLM backend: {llm}")
            raise

        except Exception as e:
            log(f"❌ [ERROR] Failed `{llm}` call")
            log(f"❌ [ERROR] Exception: {e}")
            raise
