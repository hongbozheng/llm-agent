import os
from dotenv import load_dotenv
from .logger import log


def check_api_keys(selected_llm: str) -> None:
    """Checks if necessary API keys for the given LLM are available."""

    load_dotenv()  # Load .env values into os.environ

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
        log("✅ All necessary API keys are present.")
    log("=" * 75)
