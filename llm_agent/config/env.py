import os
from dotenv import load_dotenv
from llm_agent.logger.logger import log_error, log_info, log_warn


def load_api_keys(selected_llm: str):
    """Checks if necessary API keys for the given LLM are available."""

    load_dotenv()  # Load .env values into os.environ

    llm_api_keys = {
        "gpt-4o": "OPENAI_API_KEY",
        "gemini": "GOOGLE_API_KEY",
        "deepseek": "DEEPSEEK_API_KEY",
    }

    flag = True

    log_info("=" * 75)
    log_info(" 🔍 Checking API keys for LLMs")
    log_info("-" * 75)

    for llm, env_var in llm_api_keys.items():
        if os.environ.get(env_var) is None:
            flag = False
            if llm == selected_llm:
                log_error(f"❌ Missing {env_var:<16} for {llm}")
                log_info("=" * 75)
                exit(1)
            else:
                log_warn(f" ⚠️ Missing {env_var:<16} for {llm}")

    if flag:
        log_info(" ✅ All necessary API keys are present")
    log_info("=" * 75)
