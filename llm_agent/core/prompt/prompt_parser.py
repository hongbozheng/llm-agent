from llm_agent.config.config import AgentConfig
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.io.writer import Writer
from typing import Optional

import json
from llm_agent.core.llm_backends import LLMClient
from llm_agent.logger.logger import log_error


class PromptParser:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg

    def parse(
            self,
            user_prompt: str,
            logger: Optional[ConversationLogger] = None,
            writer: Optional[Writer] = None,
    ) -> dict:
        """Uses an LLM to extract domain, intent, and constraints from the user input."""

        system_prompt = (
            "You are an intelligent financial assistant. "
            "Extract the user's primary domain "
            "(e.g., 'crypto', 'real-estate', 'stock', 'hft'), "
            "their intent (e.g., long-term investing, passive income), "
            "and any constraints (e.g., capital, risk level, frequency). "
            "Respond with STRICT JSON only:\n"
            '{"domain": "...", "intent": "...", "constraints": {...}}'
        )

        response = LLMClient.call(
            llm=self.cfg.llm,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=self.cfg.max_tokens,
            temperature=self.cfg.temperature,
            top_p=self.cfg.top_p,
        )

        try:
            prompt = json.loads(response)
        except Exception as e:
            log_error(f"❌ Failed to parse LLM response into JSON")
            log_error(f"❌ Exception `{e}`")
            raise

        if logger is not None:
            logger.log_system(prompt=system_prompt)
            logger.log_user(prompt=user_prompt)
            logger.log_llm(response=json.dumps(prompt, indent=2))

        if writer is not None:
            writer.save_json(obj=prompt, name="prompt")

        return prompt
