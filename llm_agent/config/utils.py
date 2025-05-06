from dataclasses import fields
from llm_agent.config import AgentConfig
from llm_agent.logger.logger import log_info


def print_cfg(cfg: AgentConfig):
    log_info("=" * 75)
    log_info(" ⚙️ Active Configuration")
    log_info("-" * 75)
    for field in fields(cfg):
        log_info(f" 🔹 {field.name}: {getattr(cfg, field.name)}")
    log_info("=" * 75)
