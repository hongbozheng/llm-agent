from llm_agent.core.logger import log
from llm_agent.core.llm_backends.registry import LLM_REGISTRY


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
            log(f"❌ [ERROR] Unsupported LLM backend: `{llm}`")
            log(f"🔧 [INFO]  Supported: {list(LLM_REGISTRY.keys())}")
            raise

        try:
            client_class = LLM_REGISTRY[llm]
            client = client_class()

            return client.call(
                model=llm,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
            )

        except Exception as e:
            log(f"❌ [ERROR] LLM call to `{llm}` failed.")
            log(f"❌ [ERROR] Exception {e}")
            raise
