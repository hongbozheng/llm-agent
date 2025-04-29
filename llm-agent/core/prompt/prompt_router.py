from ..logger import log
from ..schema import Prompt
from .domain_registry import DOMAIN_REGISTRY
from .prompt_parser import PromptParser


class PromptRouter:
    def __init__(self, parser: PromptParser = None) -> None:
        self.parser = parser or PromptParser()

    def route(self, user_input: str) -> dict:
        prompt: Prompt = self.parser.parse(user_input)

        domain = prompt.domain
        if domain not in DOMAIN_REGISTRY:
            log(f"❌ [ERROR] Unsupported domain: {domain}.")
            raise

        domain_handler = DOMAIN_REGISTRY[domain]()
        return domain_handler.handle_prompt(prompt)
