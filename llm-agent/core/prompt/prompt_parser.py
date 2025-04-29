import json
from ..llm.llm_client import LLMClient
from ..logger import log
from ..schema import Prompt


class PromptParser:
    def __init__(self, model: str, top_p: float):
        self.model = model
        self.top_p = top_p

    def parse(self, user_prompt: str) -> Prompt:
        system_prompt = (
            "You are an intelligent financial assistant. "
            "Extract the domain (e.g., 'crypto', 'real_estate'), the user's intent, "
            "and constraints (e.g., risk tolerance, budget, frequency). "
            "Respond in strict JSON: "
            '{"domain": "...", "intent": "...", "constraints": {...}}'
        )

        response = LLMClient.call(
            llm=self.model,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            top_p=self.top_p,
        )

        try:
            prompt = json.loads(response)
            return Prompt(
                domain=prompt["domain"].lower(),
                intent=prompt["intent"],
                constraints=prompt.get("constraints", {}),
                prompt=user_prompt,
            )
        except Exception as e:
            log(f"❌ [ERROR]: Failed to parse LLM response into structured data.")
            log(f"❌ [ERROR]: Exception `{e}`.")
            raise
