import argparse
import json
import os
import re
import openai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_gpt_to_execute_step_with_files(plan, step_index, output_file_paths, llm_model): # gpt-4o , deepseek-chat
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
    if llm_model == "gpt-4o":
        response = openai.chat.completions.create(
            model=llm_model,
            messages=[{"role": "system", "content": system_prompt}],
            temperature=0.5
        )
    elif llm_model == "deepseek-chat":
        load_dotenv()
        deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
        client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                
            ],
            stream=False
        )
    content = response.choices[0].message.content.strip()
    match = re.search(r"```python(.*?)```", content, re.DOTALL)
    return match.group(1).strip() if match else content


def run_strategy_steps(plan_path,llm_model):
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
        code = ask_gpt_to_execute_step_with_files(plan, i, step_outputs,llm_model)

        if code:
            output_path = f"step/step_{i:02d}_output.py"
            os.makedirs("step", exist_ok=True)
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
            except Exception as e:
                print(f"[ERROR] Code execution failed at step {i}: {e}")

    # Update plan with new gpt_output_file entries
    with open(plan_path, "w") as f:
        json.dump(plan, f, indent=2)
    print(f"\n[INFO] Strategy plan updated with output paths.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True, help="Path to strategy plan JSON")
    args = parser.parse_args()
    llm_model_choice = "deepseek-chat" # gpt-4o , deepseek-chat
    run_strategy_steps(args.plan,llm_model_choice)

