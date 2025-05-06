from llm_agent.core.llm_backends.registry import LLM_REGISTRY
from llm_agent.logger.logger import log_error, log_info


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
            log_error(f"❌ Unsupported LLM backend: `{llm}`")
            log_info(f" 🔧 Supported: {list(LLM_REGISTRY.keys())}")
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
            log_error(f"❌ LLM call to `{llm}` failed")
            log_error(f"❌ Exception {e}")
            raise
