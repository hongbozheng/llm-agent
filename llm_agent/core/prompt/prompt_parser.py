import json
from llm_agent.config.config import AgentConfig
from llm_agent.core.llm_backends import LLMClient
from llm_agent.core.logger import log
from llm_agent.core.prompt.schema import Prompt


class PromptParser:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg

    def parse(self, user_prompt: str) -> Prompt:
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
            print(prompt)
            return Prompt(
                domain=prompt["domain"].lower(),
                intent=prompt["intent"],
                constraints=prompt.get("constraints", {}),
                prompt=user_prompt,
            )
        except Exception as e:
            log(f"[ERROR] ❌ Failed to parse LLM response into structured data")
            log(f"[ERROR] ❌ Exception `{e}`")
            raise
