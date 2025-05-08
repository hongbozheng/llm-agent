import json
from llm_agent.config import AgentConfig
from llm_agent.core.llm_backends import LLMClient
from llm_agent.core.prompt.schema import Prompt
from llm_agent.core.utils.parser import extract_block
from llm_agent.logger.logger import log_error


def generate_strategy(cfg: AgentConfig, prompt: Prompt) -> dict:
    """Uses LLM to generate a domain-specific stock trading strategy plan."""

    system_prompt = (
        "You are a professional quantitative trading strategist with experience in equities. "
        "Given the user's goal, generate a detailed trading strategy in JSON format. "
        "Focus on being realistic, executable, and explainable to a trader. "
        "Ensure it contains clear entry/exit logic, risk controls, asset focus, and holding time."
    )

    user_prompt = (
        f"User prompt: `{prompt.prompt}`\n"
        f"Domain: {prompt.domain}\n"
        f"Intent: {prompt.intent}\n"
        f"Constraints: {prompt.constraints}\n\n"
        f"Please respond in the following JSON structure:\n"
        "{\n"
        "  'strategy-name': str,\n"
        "  'asset': str,\n"
        "  'entry-logic': str,\n"
        "  'exit-logic': str,\n"
        "  'risk-management': str,\n"
        "  'holding-period': str,\n"
        "  'notes': str\n"
        "}"
    )

    response = LLMClient.call(
        llm=cfg.llm,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        max_tokens=cfg.max_tokens,
        temperature=cfg.temperature,
        top_p=cfg.top_p,
    )

    response = extract_block(text=response, language="json")

    try:
        strategy = json.loads(response)
    except Exception as e:
        log_error(f"❌ Failed to parse LLM response into JSON")
        log_error(f"❌ Exception `{e}`")
        raise

    print(json.dumps(strategy, indent=2))

    return strategy
