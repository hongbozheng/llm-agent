from llm_agent.core.prompt.schema import Prompt


def generate_strategy(prompt: Prompt) -> dict:
    """Mock strategy builder — replace with actual LLM-generated logic."""
    risk = prompt.constraints.get("risk", "medium")
    capital = prompt.constraints.get("capital", "10000")

    return {
        "entry": "Buy BTC when RSI < 30",
        "exit": "Sell when RSI > 70",
        "risk": risk,
        "capital": capital,
        "frequency": "daily",
    }
