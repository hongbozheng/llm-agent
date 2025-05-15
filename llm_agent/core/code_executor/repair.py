from llm_agent.config import AgentConfig
from pathlib import Path
from typing import Optional

from llm_agent.core.llm_backends.llm_client import LLMClient
from llm_agent.core.utils import extract_block
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.logger.logger import log_error


def fix_code(
        cfg: AgentConfig,
        file_path: Path,
        error: str,
        logger: Optional[ConversationLogger] = None,
):
    with open(file=file_path, mode='r', encoding="utf-8") as f:
        code = f.read()
    print(error)
    system_prompt = (
        "You are a Python quant developer. The user has provided backtest code that failed. "
        "Fix the issue based on the error message and return corrected code.\n"
        "Wrap the whole script in a single code block like:\n"
        "```python\n"
        "# fixed script here\n"
        "```"
    )

    user_prompt = f"""
Original Code:
```python
{code.strip()}
```

Error Message:
{error}
""".strip()

    response = LLMClient.call(
        llm=cfg.llm,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=cfg.max_tokens,
        temperature=cfg.temperature,
        top_p=cfg.top_p,
    )

    try:
        code = extract_block(text=response, language="python")
    except Exception as e:
        log_error(f"❌ Failed to parse LLM response into Python")
        log_error(f"❌ Exception `{e}`")
        raise

    with open(file=file_path, mode='w', encoding="utf-8") as f:
        f.write(code)

    if logger is not None:
        logger.log_system(prompt=system_prompt)
        logger.log_user(prompt=user_prompt)
        logger.log_llm(response=code)
