from typing import Dict, Optional

from step_generator import ask_gpt_for_strategy_step
from step_generator import sanitize_prompt_for_filename
# from step_executor import ask_gpt_to_execute_step_with_files
from step_executor import run_strategy_steps
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
            save_path = os.path.join("step_outputs", filename)

            # Ensure the output folder exists
            os.makedirs("step_outputs", exist_ok=True)

            with open(save_path, "w") as f:
                f.write(pretty_json)

            print(f"[INFO] Saved strategy plan to: {save_path}")
    elif  args.step == "full_pipeline":
        # procedure 1 : generate step 
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
            # procedure 2: generate step code and execute 
            run_strategy_steps(save_path,args.llm_model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the T2I pipeline.")

    # I) Run Step choices & initial prompt
    parser.add_argument("--step", choices=[
        "generate_step", "evaluate_initial", "full_pipeline"
    ], required=True)    
    # gpt-4o , deepseek-chat
    parser.add_argument("--llm_model", type=str, default="gpt-4o", help="The LLM model to use (e.g., gpt-4o, deepseek-chat).")

    parser.add_argument("--question", type=str, required=True, help="The finance question to generate a strategy plan for.")
    args = parser.parse_args()
    main(args)
# python3 src/pipeline.py   --step full_pipeline   --llm_model gpt-4o   --question "What's a good momentum strategy for NVDA over the past 3 months?"