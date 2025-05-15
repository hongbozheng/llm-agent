from dataclasses import dataclass


@dataclass
class Prompt:
    domain: str
    intent: str
    constraints: dict[str, str]
    prompt: str
