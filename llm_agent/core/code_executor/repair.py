from llm_agent.config import AgentConfig
from llm_agent.core.llm_backends.llm_client import LLMClient
from llm_agent.core.utils import extract_block


def fix_code(cfg: AgentConfig, file_path: str, error: str):
    with open(file=file_path, mode='r', encoding="utf-8") as f:
        code = f.read()
    print(error)
    system_prompt = (
        "You are a Python quant developer. The user has provided backtest code that failed. "
        "Fix the issue based on the error message and return corrected code.\n"
        "Wrap the whole script in a single code block like:"
        "```python\n"
        "# fixed script here\n"
        "```"
    )

    user_prompt = f"""
Original Code:
```python
{code}
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

    code = extract_block(text=response, language="python")

    with open(file=file_path, mode='w', encoding="utf-8") as f:
        f.write(code)

    return code
