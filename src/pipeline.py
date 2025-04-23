from typing import Dict, Optional

from step_generator import ask_gpt_for_strategy_step
from step_generator import sanitize_prompt_for_filename
# from step_executor import ask_gpt_to_execute_step_with_files
from step_executor import run_strategy_steps
from step_executor import compare_strategy_summaries
import argparse
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


def main(args):
    print(args)

    if args.step == "generate_step":
        result = ask_gpt_for_strategy_step(args.question)
        time.sleep(10)
        if result:
            print("[INFO] Strategy Plan:")
            pretty_json = json.dumps(result, indent=2)
            print(pretty_json)

            safe_prompt = sanitize_prompt_for_filename(args.question)
            filename = f"strategy_plan_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_path = os.path.join("outputs", filename)

            # Ensure the output folder exists
            os.makedirs("outputs", exist_ok=True)

            with open(save_path, "w") as f:
                f.write(pretty_json)

            print(f"[INFO] Saved strategy plan to: {save_path}")
    elif  args.step == "full_pipeline":
        # procedure 1 : generate step 
        agent_model = args.llm_model
        result = ask_gpt_for_strategy_step(args.question,llm_model = agent_model)
        time.sleep(10)
        if result:
            print("[INFO] Strategy Plan:")
            pretty_json = json.dumps(result, indent=2)
            print(pretty_json)

            safe_prompt = sanitize_prompt_for_filename(args.question)
            filename = f"strategy_plan_{agent_model}_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            save_path = os.path.join("outputs", filename)

            # Ensure the output folder exists
            os.makedirs("outputs", exist_ok=True)

            with open(save_path, "w") as f:
                f.write(pretty_json)

            print(f"[INFO] Saved strategy plan to: {save_path}")
            # procedure 2: generate step code and execute 
            run_strategy_steps(save_path,args.llm_model)
    elif args.step == "compare_agents":
        summary_paths = []
        for agent_model in ["gpt-4o", "deepseek-chat"]:
            print(f"\n=== Running strategy for: {agent_model} ===")
            result = ask_gpt_for_strategy_step(args.question, llm_model=agent_model)
            time.sleep(10)
            if result:
                pretty_json = json.dumps(result, indent=2)
                safe_prompt = sanitize_prompt_for_filename(args.question)
                filename = f"strategy_plan_{agent_model}_{safe_prompt}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                plan_path = os.path.join("outputs", filename)

                os.makedirs("outputs", exist_ok=True)
                with open(plan_path, "w") as f:
                    f.write(pretty_json)
                print(f"[INFO] Saved strategy plan to: {plan_path}")

                # run_strategy_steps(plan_path, agent_model)

                # # Assume summary saving will be added to run_strategy_steps()
                # summary_path = plan_path.replace("outputs", "summaries").replace("strategy_plan", "summary")
                # summary_paths.append(summary_path)

                summary_path = run_strategy_steps(plan_path, agent_model)
                summary_paths.append(summary_path)

        # Step 3: Use GPT-4o to compare
        if len(summary_paths) == 2:
            
            compare_strategy_summaries(summary_paths[0], summary_paths[1], args.question)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the T2I pipeline.")

    # I) Run Step choices & initial prompt
    parser.add_argument("--step", choices=[
        "generate_step", "evaluate_initial", "full_pipeline","compare_agents"
    ], required=True)    
    # gpt-4o , deepseek-chat
    parser.add_argument("--llm_model", type=str, default="gpt-4o", help="The LLM model to use (e.g., gpt-4o, deepseek-chat, gemini-1.5-flash).")

    parser.add_argument("--question", type=str, required=True, help="The finance question to generate a strategy plan for.")
    args = parser.parse_args()
    main(args)
# python3 src/pipeline.py   --step full_pipeline   --llm_model gpt-4o   --question "What's a good strategy for MAXN for the next 1 months?"
# python3 src/pipeline.py   --step compare_agents   --llm_model gpt-4o   --question "What's a good momentum strategy for TSLA over the past 3 months?"