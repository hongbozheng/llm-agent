import argparse
import json
import os
import re
import openai
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

import google.generativeai as genai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # <-- Get Google API Key

# --- Configure Gemini ---
if GOOGLE_API_KEY:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        print("[INFO] Gemini API configured successfully.")
    except Exception as e:
        print(f"[WARN] Failed to configure Gemini API: {e}")
else:
    print(
        "[WARN] GOOGLE_API_KEY not found in .env file. Gemini models will not be available.")


# -----------------------
def ask_gpt_to_execute_step_with_files(plan, step_index, output_file_paths,
                                       llm_model):  # gpt-4o , deepseek-chat
    question = plan["question"]
    current_step = plan["steps"][step_index]

    prev_context = []
    for i, path in enumerate(output_file_paths):
        try:
            with open(path, "r") as f:
                content = f.read()
                prev_context.append(f"Step {i} result:\n{content}")
        except:
            prev_context.append(f"Step {i} result: [Failed to load {path}]")

    system_prompt = f"""
You are a quantitative trading assistant helping to build a strategy.

User's original question:
{question}

Steps completed so far:
{chr(10).join(prev_context)}

Current step:
- {current_step['step']}
- Reasoning: {current_step['reasoning']}

Please generate Python code that completes this step, based on all context so far.
Respond ONLY with a code block.
""".strip()
    if step_index == len(plan["steps"]) - 1:
        system_prompt += (
            "\n\nAt the end of this step, please output a Python dictionary called `strategy_info` "
            "with the following fields: strategy_type, assets, lookback_days, indicators, evaluation_metrics."
            "\nRespond only with a code block as before."
        )
    if llm_model == "gpt-4o":
        response = openai.chat.completions.create(
            model=llm_model,
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.5
        )
    elif llm_model == "deepseek-chat":
        load_dotenv()
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        client = OpenAI(api_key=deepseek_api_key,
                        base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},

            ],
            stream=False
        )
    elif llm_model.startswith("gemini"):
        print(f"[INFO] Calling Gemini model: {llm_model}")
        if not GOOGLE_API_KEY:
            raise ValueError(
                "GOOGLE_API_KEY not found or Gemini API not configured.")

        # Gemini uses only one prompt string
        full_prompt = system_prompt
        model = genai.GenerativeModel(llm_model)
        response = model.generate_content(
            full_prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7
            )
        )

        if not response.candidates:
            raise ValueError(
                f"Gemini response was blocked. Prompt feedback: {response.prompt_feedback}")

    if llm_model.startswith("gemini"):
        content = response.text.strip()
        if content.startswith("```json"):
            content = content[len("```json"):].strip()
        if content.startswith("```python"):
            content = content[len("```python"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()
    elif llm_model.startswith("gpt") or llm_model.startswith("deepseek"):
        content = response.choices[0].message.content.strip()
        if content.startswith("```") and content.endswith("```"):
            content = content[
                      content.find('\n') + 1: content.rfind('```')].strip()

    match = re.search(r"```python(.*?)```", content, re.DOTALL)
    return match.group(1).strip() if match else content


def run_strategy_steps(plan_path, llm_model):
    with open(plan_path, "r") as f:
        plan = json.load(f)

    step_outputs = []
    steps = plan.get("steps", [])
    exec_globals = {}
    for i, step in enumerate(steps):
        print(f"\n==============================")
        print(f"🔧 Executing Step {i}: {step['step']}")
        print(f"==============================")

        # Ask GPT with context from previous step output files
        code = ask_gpt_to_execute_step_with_files(plan, i, step_outputs,
                                                  llm_model)

        if code:
            # output_path = f"step/step_{i:02d}_output.py"
            # os.makedirs("step", exist_ok=True)
            # with open(output_path, "w") as f:
            #     f.write(code)
            # print(f"[INFO] Saved step {i} output to: {output_path}")
            # Create a subdirectory for the current LLM
            step_dir = os.path.join("step", llm_model)
            os.makedirs(step_dir, exist_ok=True)

            output_path = os.path.join(step_dir, f"step_{i:02d}_output.py")
            with open(output_path, "w") as f:
                f.write(code)

            print(f"[INFO] Saved step {i} output to: {output_path}")

            # Store file path for use in next step context
            step_outputs.append(output_path)
            step["gpt_output_file"] = output_path

            # Try executing the generated code
            try:
                # exec_globals = {}
                exec(code, exec_globals)
                print(f"[SUCCESS] Executed step {i} successfully.")
                strategy_info = exec_globals.get("strategy_info")
                if strategy_info:
                    step["strategy_info"] = strategy_info
                    print(f"[INFO] Extracted strategy_info from step {i}.")
            except Exception as e:
                print(f"[ERROR] Code execution failed at step {i}: {e}")

    # Update plan with new gpt_output_file entries
    # with open(plan_path, "w") as f:
    #     json.dump(plan, f, indent=2)
    # print(f"\n[INFO] Strategy plan updated with output paths.")
    # Build summary content so we can later compare two LLM results
    summary = {
        "question": plan["question"],
        "steps": []
    }

    for i, step in enumerate(steps):
        code = ""
        output_path = step.get("gpt_output_file")
        if output_path and os.path.exists(output_path):
            with open(output_path, "r") as f:
                code = f.read()

        summary_step = {
            "step": step["step"],
            "reasoning": step["reasoning"],
            "code": code
        }
        if "strategy_info" in step:
            summary_step["strategy_info"] = step["strategy_info"]

        summary["steps"].append(summary_step)

    # Save summary
    os.makedirs("summaries", exist_ok=True)
    safe_prompt = re.sub(r'\s+', '_', plan["question"]).strip()[:100]
    summary_filename = f"summary_{llm_model}_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    summary_path = os.path.join("summaries", summary_filename)

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n✅ [INFO] Full summary saved to: {summary_path}")
    return summary_path


# Helper for comparing LLM results
def compare_strategy_summaries(summary_path_1, summary_path_2, question):
    # Load both summaries
    with open(summary_path_1, "r") as f:
        summary_1 = json.load(f)
    with open(summary_path_2, "r") as f:
        summary_2 = json.load(f)

    # Convert both summaries to string
    def format_summary(summary, label):
        result = f"### Strategy from {label}\n"
        result += f"**Question**: {summary['question']}\n\n"
        for i, step in enumerate(summary["steps"]):
            result += f"**Step {i + 1}: {step['step']}**\n"
            result += f"- Reasoning: {step['reasoning']}\n"
            result += f"- Code:\n```\n{step['code']}\n```\n\n"
        return result

    summary_text_1 = format_summary(summary_1, "GPT-4o")
    summary_text_2 = format_summary(summary_2, "DeepSeek")

    # Final prompt
    system_prompt = "You are a financial strategy analyst. Compare two strategies generated by different LLM agents."
    user_prompt = f"""
Compare the two strategies below for the following finance question:
**{question}**

Instructions:
- Evaluate clarity and reasoning of the steps
- Evaluate usefulness and correctness of the code
- Choose the better strategy and explain why
- Provide a one-paragraph natural language summary as final judgment

{summary_text_1}

{summary_text_2}
"""

    print("\n[INFO] Asking GPT-4o to compare strategies...")

    # Send to GPT-4o
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()
    print("\n===== 🧠 Comparison Result =====")
    print(content)

    # Optionally save to file
    os.makedirs("comparisons", exist_ok=True)
    safe_name = re.sub(r'\s+', '_', question.strip())[:100]
    filename = f"compare_{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    path = os.path.join("comparisons", filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"\n✅ [INFO] Comparison saved to: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True,
                        help="Path to strategy plan JSON")
    args = parser.parse_args()
    llm_model_choice = "deepseek-chat"  # gpt-4o , deepseek-chat
    run_strategy_steps(args.plan, llm_model_choice)