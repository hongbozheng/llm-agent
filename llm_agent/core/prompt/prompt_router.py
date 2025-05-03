from llm_agent.config.config import AgentConfig
from llm_agent.core.logger import log
from llm_agent.core.prompt import DOMAIN_REGISTRY
from llm_agent.core.prompt.prompt_parser import PromptParser
from llm_agent.core.prompt.schema import Prompt


class PromptRouter:
    """Routes parsed prompts to the appropriate domain handler."""

    def __init__(self, cfg: AgentConfig):
        self.parser = PromptParser(cfg=cfg)

    def route(self, user_prompt: str) -> dict:
        try:
            prompt: Prompt = self.parser.parse(user_prompt=user_prompt)
            domain = prompt.domain

            if domain not in DOMAIN_REGISTRY:
                log(f"❌ [ERROR] Unsupported domain: `{domain}`")
                log(f"🔧 [INFO]  Supported: {list(DOMAIN_REGISTRY.keys())}")
                raise

            handler_class = DOMAIN_REGISTRY[domain]
            handler = handler_class()

            return handler.handle_prompt(prompt=prompt)

        except Exception as e:
            log(f"❌ [ERROR] Routing failed for prompt.")
            log(f"❌ [ERROR] Exception: {e}")
            raise
