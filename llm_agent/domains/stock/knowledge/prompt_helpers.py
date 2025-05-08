from llm_agent.domains.stock.knowledge.rules import COMMON_MISTAKES


def get_coding_advice() -> str:
    """
    Return formatted string with LLM backtest coding mistakes and how to avoid them.
    """
    sections = [
        "You are writing Python code for backtesting a stock strategy.",
        "Here are common mistakes you MUST avoid:"
    ]

    for i, rule in enumerate(COMMON_MISTAKES):
        sections.append(
            f"{i+1}. ❌ {rule['mistake']}\n   ✅ {rule['fix']}"
        )

    return "\n\n".join(sections)
