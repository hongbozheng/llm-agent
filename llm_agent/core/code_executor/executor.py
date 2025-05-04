from llm_agent.config.config import AgentConfig
from llm_agent.core.code_executor.repair import fix_code
from llm_agent.core.code_executor.runner import exec_code
from llm_agent.core.logger import log


class CodeExecutor:
    def __init__(self, cfg: AgentConfig):
        self.cfg = cfg

    def execute(self, file_path: str):
        attempt = 0

        while attempt < self.cfg.attempts:
            log(f"[INFO]  🚀 Attempt {attempt + 1} Executing `{file_path}`")
            success, output = exec_code(file_path=file_path, timeout=self.cfg.timeout)

            if success:
                log(f"[INFO]  ✅ `{file_path}` executed successfully")
            else:
                log(f"[ERROR] ❌ `{file_path}` execution failed")

                log(f"[INFO]  🛠 Attempting to fix code")
                _ = fix_code(cfg=self.cfg, file_path=file_path, error=output)

                log(f"[INFO]  🔁 Retrying updated code")
                log("~" * 75)
                attempt += 1

        log("[INFO]  🛑 Maximum attempts reached")
