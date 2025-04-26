from typing import Tuple

import contextlib
import io
import re
import subprocess
import threading
from llm_client import call_llm
from logger import log, log_output


class CodeExecutor:
    def __init__(self, mode: str, timeout: int) -> None:
        if mode not in {"process", "thread"}:
            log("❌ [ERROR] Mode must be `process` or `thread`")
        self.mode = mode
        self.timeout = timeout
        self.global_ctx = {}

        return

    def exec(self, file_path: str) -> Tuple[bool, str]:
        if self.mode == "process":
            return self._exec_process(file_path)
        else:
            return self._exec_thread(file_path)

    def _exec_process(self, file_path: str) -> Tuple[bool, str]:
        try:
            result = subprocess.run(
                ["python3", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout,
            )
            success = result.returncode == 0
            output = result.stdout + "\n" + result.stderr
            return success, output.strip()

        except subprocess.TimeoutExpired:
            return False, f"Execution timed out after {self.timeout}s"
        except Exception as e:
            return False, f"Unexpected execution error: {type(e).__name__} {str(e)}"

    def _exec_thread(self, file_path: str) -> Tuple[bool, str]:
        output_buf = io.StringIO()

        def runner():
            try:
                file = open(file_path, 'r')
                code = file.read()
                file.close()

                with contextlib.redirect_stdout(output_buf), contextlib.redirect_stderr(output_buf):
                    exec(code, self.global_ctx)

            except Exception as e:
                output_buf.write(f"Execution error: {type(e).__name__}: {str(e)}")

        thread = threading.Thread(target=runner)
        thread.start()
        thread.join(timeout=self.timeout)

        if thread.is_alive():
            return False, f"Execution timed out after {self.timeout}s"

        output = output_buf.getvalue().strip()
        success = "Execution error" not in output

        return success, output


def fix_code(llm, temp, file_path, output):
    f = open(file=file_path, mode='r')
    code = f.read()
    f.close()

    sys_prompt = f"""
You are an expert Python code debugger and code generator.

You will receive a piece of broken Python code along with its error messages.

Your job is to:
- Understand the code and the error.
- Fix the code so that it can run successfully without errors.
- Maintain the original intent and functionality of the code as much as possible.
- Output the corrected Python code, with any explanations, comments, or markdown formatting.
""".strip()

    usr_prompt = f"""
Here is the broken Python code:

{code}

And here is the error message:

{output}
""".strip()

    content = call_llm(llm, sys_prompt, usr_prompt, temp)

    if llm == "gpt-4o" or llm == "deepseek":
        if content.startswith("```") and content.endswith("```"):
            content = content[
                      content.find('\n') + 1: content.rfind('```')].strip()
    elif llm.startswith("gemini"):
        content = content.text.strip()
        if content.startswith("```json"):
            content = content[len("```json"):].strip()
        if content.startswith("```python"):
            content = content[len("```python"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

    match = re.search(r"```python(.*?)```", content, re.DOTALL)
    return match.group(1).strip() if match else content


def exec_debug(
        mode: str,
        timeout: int,
        max_att: int,
        llm: str,
        temp: float,
        file_path: str,
) -> bool:
    """
        Try executing the file, and if it fails, ask LLM to fix it.
        Repeat until success or maximum attempts are reached.

        Returns:
            True if success, False if failed after retries.
        """
    att = 0
    executor = CodeExecutor(mode, timeout)

    while att < max_att:
        log(f"🚀 Attempt {att + 1} Executing `{file_path}`")
        success, output = executor.exec(file_path)

        if success:
            log(f"✅ Code executed successfully")
            log_output(f"🖨️ Output\n{output}")
            return True
        else:
            log(f"❌ Code execution failed")
            log_output(f"🛠️ Error\n{output}")

            log(f"🛠 Attempting to fix code")
            code = fix_code(llm, temp, file_path, output)

            f = open(file_path, 'w')
            f.write(code)
            f.close()

            log(f"🔁 Updated code. Retrying")
            log("~" * 75)
            att += 1

    log("🛑 Maximum attempts reached")

    return False
