import re
from llm_agent.core.logger import log


def extract_block(text: str, language: str) -> str:
    """
    Extracts the first code block of a given language from an LLM response.

    Supports blocks like:
    ```python
    <code>
    ```

    Args:
        text (str): The full LLM response.
        language (str): The language identifier inside the triple backticks.

    Returns:
        str: Extracted raw code block without backticks.

    Raises:
        ValueError: If no matching code block is found.
    """
    pattern = rf"```{language}\s*\n(.*?)```"

    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    log(f"[ERROR] ❌ No `{language}` block found")
    raise
