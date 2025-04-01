from typing import Dict, Optional

from step_generator import ask_gpt_for_strategy_step
from step_generator import sanitize_prompt_for_filename
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
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the T2I pipeline.")

    # I) Run Step choices & initial prompt
    parser.add_argument("--step", choices=[
        "generate_step", "evaluate_initial", "full_pipeline"
    ], required=True)    
    args = parser.parse_args()
    main(args)