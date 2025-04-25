import google.generativeai as genai # Add Gemini import
import json
import openai
import os
from logger import log, log_prompt
from openai import OpenAI # for deepseek


def generate_strategy(llm: str, prompt: str):
    """
    Ask GPT a finance-related question and get back a structured JSON strategy plan.
    """

    system_prompt = f"""
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
  "question": "{prompt}",
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

    user_prompt = f"Question {prompt}\nPlease respond in valid JSON format only."

    log_prompt(system_prompt, user_prompt)

    strategy = None

    try:
        if llm == "gpt-4o":
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.chat.completions.create(
                model=llm,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
        elif llm == "deepseek":
            deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
            client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
        elif llm.startswith("gemini"):
            api_key = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=api_key)
            # Combine prompts for Gemini's generate_content (simpler API)
            full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"
            model = genai.GenerativeModel(llm)
            # Optional: Add safety settings if needed
            # safety_settings=[...]
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    # Ensure Gemini outputs JSON
                    # response_mime_type="application/json", # Use if model supports enforced JSON
                    temperature=0.7,
                )
                # safety_settings=safety_settings
            )
            # Check for blocked response
            if not response.candidates:
                 raise ValueError(f"Gemini response was blocked. Prompt feedback: {response.prompt_feedback}")
            content = response.text.strip()
        else:
            raise ValueError(f"Unsupported model: {llm}")

        # content = response.choices[0].message.content.strip()

        # # Clean up triple backticks if included
        # if content.startswith("```") and content.endswith("```"):
        #     content = content[content.find('\n') + 1: content.rfind('```')].strip()

        if llm.startswith("gemini"):
            content = response.text.strip()  
            if content.startswith("```json"):
                content = content[len("```json"):].strip()
            if content.endswith("```"):
                content = content[:-3].strip()
        else:
            content = response.choices[0].message.content.strip()
            if content.startswith("```") and content.endswith("```"):
                content = content[content.find('\n') + 1: content.rfind('```')].strip()

        # print(f"[DEBUG] LLM Response:\n{content}")

        strategy = json.loads(content)

    except Exception as e:
        log("[❌] [ERROR] No strategy plan generated from LLM.")

    return strategy


# if __name__ == "__main__":
#     llm_model = "gemini-1.5-flash" #option gpt-4o, deepseek-chat,gemini-pro,gemini-1.5-flash
#     question = "What's a good momentum trading strategy for APPL over the past week?"
#     result = ask_for_strategy(question,llm_model)
#     time.sleep(10)
#     if result:
#         print("[INFO] Strategy Plan:")
#         pretty_json = json.dumps(result, indent=2)
#         print(pretty_json)
#
#         safe_prompt = sanitize_prompt_for_filename(question)
#         filename = f"strategy_plan_{llm_model}_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
#         save_path = os.path.join("step_outputs", filename)
#
#         # Ensure the output folder exists
#         os.makedirs("step_outputs", exist_ok=True)
#
#         with open(save_path, "w") as f:
#             f.write(pretty_json)
#
#         print(f"[INFO] Saved strategy plan to: {save_path}")
