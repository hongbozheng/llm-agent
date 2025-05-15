from llm_agent.config.config import AgentConfig
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.io.writer import Writer
from typing import Optional

from llm_agent.core.prompt import DOMAIN_REGISTRY
from llm_agent.core.prompt.prompt_parser import PromptParser
from llm_agent.core.prompt.schema import Prompt
from llm_agent.logger.logger import log_error, log_info


class PromptRouter:
    """Routes parsed prompts to the appropriate domain handler."""

    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg
        self.parser = PromptParser(cfg=cfg)

    def route(
            self,
            user_prompt: str,
            logger: Optional[ConversationLogger] = None,
            writer: Optional[Writer] = None,
    ) -> dict:
        try:
            prompt = self.parser.parse(
                user_prompt=user_prompt, logger=logger, writer=writer,
            )

            prompt = Prompt(
                domain=prompt["domain"].lower(),
                intent=prompt["intent"],
                constraints=prompt.get("constraints", {}),
                prompt=user_prompt,
            )
            domain = prompt.domain

            if domain not in DOMAIN_REGISTRY:
                log_error(f"❌ Unsupported domain: `{domain}`")
                log_info(f" 🔧 Supported: {list(DOMAIN_REGISTRY.keys())}")
                raise

            handler_class = DOMAIN_REGISTRY[domain]
            handler = handler_class(cfg=self.cfg)

            return handler.process_prompt(
                prompt=prompt, logger=logger, writer=writer
            )

        except Exception as e:
            log_error(f"❌ Routing failed for prompt")
            log_error(f"❌ Exception: {e}")
            raise
