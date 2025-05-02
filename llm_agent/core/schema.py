from dataclasses import dataclass
from typing import Dict


@dataclass
class Prompt:
    domain: str
    intent: str
    constraints: Dict[str, str]
    prompt: str
