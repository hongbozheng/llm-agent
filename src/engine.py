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

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt_for_strategy(
    finance_question: str,
    llm_model: str = "gpt-4o" 
):
    """
    Ask GPT a finance-related question and get back a structured JSON strategy plan.
    """

    # System prompt to enforce JSON structure
    system_prompt = (
        "You are a quantitative finance assistant. "
        "When the user asks a question, respond with a complete strategy plan with several steps in JSON format. "
        "Your output must be a JSON object that includes 1. steps for generating the strategy 2. strategy it self : strategy_type, assets, lookback_days, indicators, "
        "evaluation_metrics, and next_steps."
    )

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
    question = "What's a good momentum trading strategy for TSLA over the past 3 months?"
    result = ask_gpt_for_strategy(question)
    time.sleep(10)
    if result:
        print("[INFO] Strategy Plan:")
        print(json.dumps(result, indent=2))
