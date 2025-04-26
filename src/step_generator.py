import json
from llm_client import call_llm
from logger import log_prompt


def generate_strategy(llm: str, prompt: str):
    """
    Ask GPT a finance-related question and get back a structured JSON strategy plan.
    """

    sys_prompt = f"""
You are a quantitative finance assistant.

Your task is to analyze the user's finance-related question:
'{prompt}'

---

**Instructions:**
- Do NOT generate a full strategy or code yet, although in the end of all steps I should get
  1. code to test my strategy
  2. strategy itself: strategy_type, assets, lookback_days, indicators, evaluation_metrics, and next_steps.
- Break the problem down into a step-by-step decision-making plan.
- For each step, explain the reasoning.
- Output strictly in JSON format.

**Example Output:**
```json
{{
  "prompt": "{prompt}",
  "strategy": [
    {{
      "action": "Identify asset and timeframe",
      "justification": "Determine which asset(s) and what historical period are relevant to the user's query."
    }},
    {{
      "action": "Select strategy type",
      "justification": "Decide whether a momentum, mean-reversion, or ML-based approach is more appropriate."
    }},
    {{
      "action": "Choose technical indicators",
      "justification": "Pick indicators like SMA, RSI based on the strategy goal."
    }},
    {{
      "action": "Define evaluation metrics",
      "justification": "Sharpe Ratio and Max Drawdown are useful to evaluate performance."
    }}
  ]
}}
""".strip()

    usr_prompt = f"Question {prompt}\nPlease respond in valid JSON format only."

    log_prompt(sys_prompt, usr_prompt)

    content = call_llm(llm, sys_prompt, usr_prompt, temp=0.7)

    if llm == "gpt-4o" or llm == "deepseek":
        if content.startswith("```") and content.endswith("```"):
            content = content[content.find('\n') + 1: content.rfind('```')].strip()
    elif llm.startswith("gemini"):
        content = content.text.strip()
        if content.startswith("```json"):
            content = content[len("```json"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

    strategy = json.loads(content)

    return strategy
