from llm_agent.config.config import AgentConfig
from pathlib import Path

from llm_agent.core.code_executor.repair import fix_code
from llm_agent.core.code_executor.runner import exec_code
from llm_agent.logger.logger import log_error, log_info


class CodeExecutor:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg

    def execute(self, file_path: Path):
        attempt = 0

        while attempt < self.cfg.attempts:
            log_info(f" 🚀 Attempt {attempt + 1} Executing `{file_path}`")
            success, output = exec_code(file_path=file_path, timeout=self.cfg.timeout)

            if success:
                log_info(f" ✅ `{file_path}` executed successfully")
                return
            else:
                log_error(f"❌ `{file_path}` execution failed")

                log_info(f" 🛠 Attempting to fix code")
                fix_code(cfg=self.cfg, file_path=file_path, error=output)

                log_info(f" 🔁 Retrying updated code")
                log_info("~" * 75)

            attempt += 1

        log_info(" 🛑 Maximum attempts reached")
