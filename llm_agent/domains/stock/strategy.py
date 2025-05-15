from llm_agent.config import AgentConfig
from llm_agent.core.prompt.schema import Prompt
from llm_agent.io.conversation_logger import ConversationLogger
from llm_agent.io.writer import Writer
from typing import Optional

import json
from llm_agent.core.llm_backends import LLMClient
from llm_agent.core.utils.parser import extract_block
from llm_agent.logger.logger import log_error, log_info


def generate_strategy(
        cfg: AgentConfig,
        prompt: Prompt,
        logger: Optional[ConversationLogger] = None,
        writer: Optional[Writer] = None,
) -> dict:
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

    if logger is not None:
        logger.log_system(prompt=system_prompt)
        logger.log_user(prompt=user_prompt)
        logger.log_llm(response=json.dumps(strategy, indent=2))

    if writer is not None:
        writer.save_json(obj=strategy, name="strategy")
        log_info(f" 📝 Save strategy to `{writer.get_path()}/strategy.json`")

    return strategy
