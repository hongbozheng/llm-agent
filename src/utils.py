import os
import re
from dotenv import load_dotenv
from logger import log


def check_api_keys(selected_llm: str) -> None:
    """Checks if necessary API keys for the given LLM are available."""

    load_dotenv()

    llm_api_keys = {
        "gpt-4o": "OPENAI_API_KEY",
        "gemini": "GOOGLE_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
    }

    flag = True

    log("=" * 75)
    log("🔍 Checking API keys for LLMs")
    log("-" * 75)

    for llm, env_var in llm_api_keys.items():
        if os.environ.get(env_var) is None:
            flag = False
            if llm == selected_llm:
                log(f"❌ [ERROR] Missing {env_var:<16} for {llm}")
                log("=" * 75)
                exit(1)
            else:
                log(f"⚠️ [WARN]  Missing {env_var:<16} for {llm}")

    if flag:
        log(f"✅ ALL LLM API keys are available")
    log("=" * 75)

    return


def sanitize_for_filename(prompt: str) -> str:
    """
    Converts a prompt string into a safe filename by:
    - Replacing all whitespace with underscores
    - Removing or replacing unsafe characters
    """
    # Replace all whitespace with underscores
    safe = re.sub(r'\s+', '_', prompt.strip())

    # Remove characters unsafe for filenames
    safe = re.sub(r'[<>:"/\\|?*]', '', safe)

    # Optional: truncate if too long
    return safe[:100]
