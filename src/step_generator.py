from typing import Dict, Optional, Tuple

import json
from llm_client import call_llm
from logger import log_prompt


def generate_strategy(
        llm: str,
        prompt: str,
        temp: float,
) -> Dict[str, Dict[str, str]]:
    """
    Ask GPT a finance-related question and get back a structured JSON strategy plan.
    """

    sys_prompt = f"""
You are a quantitative finance assistant. Your task is to analyze the user's finance-related question.

Instructions:
- Do NOT generate a full strategy or code yet, although in the end of all steps I should get
  1. code to test my strategy
  2. strategy itself: strategy_type, assets, lookback_days, indicators, evaluation_metrics, and next_steps.
- Break the problem down into a step-by-step decision-making plan.
- For each step, explain the reasoning.
- Output strictly in JSON format.

Example Output:
```json
{{
  "prompt": "Design a high-frequency trading strategy for the NASDAQ 100 index futures, focusing on short-term mean-reversion within a 5-minute timeframe.",
  "strategy": [
    {{
      "action": "Identify asset and timeframe",
      "justification": "Focus on NASDAQ 100 index futures (NQ) using a 5-minute bar timeframe to capture intraday micro-movements suitable for HFT."
    }},
    {{
      "action": "Select strategy type",
      "justification": "A mean-reversion approach is appropriate for short-term inefficiencies in liquid, high-volume instruments like index futures."
    }},
    {{
      "action": "Choose technical indicators",
      "justification": "Use indicators sensitive to short-term price deviations, such as Z-Score of mid-price returns, VWAP deviations, or fast RSI (e.g., 2-period RSI)."
    }},
    {{
      "action": "Define evaluation metrics",
      "justification": "Metrics such as Profit per Trade, Sharpe Ratio (intraday), and Maximum Drawdown are critical for HFT performance evaluation."
    }},
    {{
      "action": "Determine execution constraints",
      "justification": "Incorporate latency considerations, slippage, and order book depth into strategy design to reflect real HFT execution challenges."
    }}
  ]
}}
""".strip()

    usr_prompt = f"Question: {prompt}"

    log_prompt(sys_prompt, usr_prompt)

    content = call_llm(llm, sys_prompt, usr_prompt, temp)

    if llm == "gpt-4o" or llm == "deepseek":
        if content.startswith("```") and content.endswith("```"):
            content = content[content.find('\n') + 1: content.rfind('```')].strip()
    elif llm.startswith("gemini"):
        content = content.text.strip()
        if content.startswith("```json"):
            content = content[len("```json"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

    convo = {
        "generate-strategy": {
            "sys-prompt": sys_prompt,
            "usr-prompt": usr_prompt,
            "llm-response": content,
        },
    }

    return convo
