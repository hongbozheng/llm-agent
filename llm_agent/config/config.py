from typing import Optional

import argparse
import yaml
from ..core.logger import log
from dataclasses import dataclass, fields


@dataclass
class AgentConfig:
    llm: str = "gpt-4o"
    max_tokens: int = 1024
    temperature: float = 0.5
    top_p: float = 0.8
    timeout: int = 60
    attempts: int = 5

    @classmethod
    def load(
            cls,
            cfg_path: str = "llm_agent/config/cfg.yaml",
            args: Optional[argparse.Namespace] = None,
    ) -> "AgentConfig":
        with open(file=cfg_path, mode='r') as f:
            cfg = yaml.safe_load(stream=f)

        cli = vars(args) if args else {}
        valid_keys = {field.name for field in fields(cls)}
        cli = {k: v for k, v in cli.items() if v is not None and k in valid_keys}
        cfg = {**cfg, **cli}

        return cls(**cfg)

    def print_summary(self):
        log("=" * 75)
        log("[INFO] 🔧 Active Configuration")
        log("-" * 75)
        for field in fields(self):
            log(f"[INFO] {field.name}: {getattr(self, field.name)}")
        log("=" * 75)
