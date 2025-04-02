from typing import List
import openai
import os
from datetime import datetime
import re
import json
import base64
from dotenv import load_dotenv
import time

import json
import re
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def sanitize_prompt_for_filename(prompt: str) -> str:
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

def ask_gpt_for_strategy_step(
    finance_question: str,
    llm_model: str = "gpt-4o" 
):
    """
    Ask GPT a finance-related question and get back a structured JSON strategy plan.
    """

    # System prompt to enforce JSON structure
    # system_prompt = (
    #     "You are a quantitative finance assistant. "
    #     "When the user asks a question, respond with a complete strategy plan with several steps in JSON format. "
    #     "Your output must be a JSON object that includes 1. steps for generating the strategy  " # 2. strategy it self : strategy_type, assets, lookback_days, indicators, "evaluation_metrics, and next_steps."
        
    # )
    system_prompt = f"""
You are a quantitative finance assistant.

Your task is to analyze the user's finance-related question:
'{finance_question}'

---

**Instructions:**
- Do NOT generate a full strategy or code yet, although in the end of all steps I shuold get 1. code to test my strategy 2.strategy it self : strategy_type, assets, lookback_days, indicators, evaluation_metrics, and next_steps.
- Break the problem down into a step-by-step decision-making plan.
- For each step, explain the reasoning.
- Output strictly in JSON format.

**Example Output:**
```json
{{
  "question": "{finance_question}",
  "steps": [
    {{
      "step": "Identify asset and timeframe",
      "reasoning": "Determine which asset(s) and what historical period are relevant to the user's query."
    }},
    {{
      "step": "Select strategy type",
      "reasoning": "Decide whether a momentum, mean-reversion, or ML-based approach is more appropriate."
    }},
    {{
      "step": "Choose technical indicators",
      "reasoning": "Pick indicators like SMA, RSI based on the strategy goal."
    }},
    {{
      "step": "Define evaluation metrics",
      "reasoning": "Sharpe Ratio and Max Drawdown are useful to evaluate performance."
    }}
  ]
}}
""".strip()
    

    user_prompt = f"Question: {finance_question}\n\nPlease respond in valid JSON format only."

    try:
        response = openai.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        print("\n" + "=" * 60)
        print("🚀 **Execution Make you rich today Strategy** 🚀")
        print("\n" + "=" * 60)
        print("System prompt")
        print(system_prompt)
        print("\n" + "=" * 60)
        print("User prompt")
        print(user_prompt)
        content = response.choices[0].message.content.strip()

        # Clean up triple backticks if included
        if content.startswith("```") and content.endswith("```"):
            content = content[content.find('\n')+1 : content.rfind('```')].strip()

        print(f"[DEBUG] GPT Response:\n{content}")

        strategy_plan = json.loads(content)
        return strategy_plan

    except Exception as e:
        print(f"[ERROR] Failed to get strategy plan from GPT: {e}")
        return None
    
if __name__ == "__main__":
    question = "What's a good momentum trading strategy for APPL over the past week?"
    result = ask_gpt_for_strategy_step(question)
    time.sleep(10)
    if result:
        print("[INFO] Strategy Plan:")
        pretty_json = json.dumps(result, indent=2)
        print(pretty_json)

        safe_prompt = sanitize_prompt_for_filename(question)
        filename = f"strategy_plan_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_path = os.path.join("step_outputs", filename)

        # Ensure the output folder exists
        os.makedirs("step_outputs", exist_ok=True)

        with open(save_path, "w") as f:
            f.write(pretty_json)

        print(f"[INFO] Saved strategy plan to: {save_path}")

